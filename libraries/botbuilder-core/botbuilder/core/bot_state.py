# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import abstractmethod
from copy import deepcopy
from typing import Callable, Dict, Union
from jsonpickle.pickler import Pickler
from botbuilder.core.state_property_accessor import StatePropertyAccessor
from .turn_context import TurnContext
from .storage import Storage
from .property_manager import PropertyManager


class CachedBotState:
    """
    Internal cached bot state.
    """

    def __init__(self, state: Dict[str, object] = None):
        self.state = state if state is not None else {}
        self.hash = self.compute_hash(state)

    @property
    def is_changed(self) -> bool:
        return self.hash != self.compute_hash(self.state)

    def compute_hash(self, obj: object) -> str:
        return str(Pickler().flatten(obj))


class BotState(PropertyManager):
    def __init__(self, storage: Storage, context_service_key: str):
        self.state_key = "state"
        self._storage = storage
        self._context_service_key = context_service_key

    def create_property(self, name: str) -> StatePropertyAccessor:
        """
        Create a property definition and register it with this BotState.
        :param name: The name of the property.
        :param force:
        :return: If successful, the state property accessor created.
        """
        if not name:
            raise TypeError("BotState.create_property(): name cannot be None or empty.")
        return BotStatePropertyAccessor(self, name)

    def get(self, turn_context: TurnContext) -> Dict[str, object]:
        cached = turn_context.turn_state.get(self._context_service_key)

        return getattr(cached, "state", None)

    async def load(self, turn_context: TurnContext, force: bool = False) -> None:
        """
        Reads in  the current state object and caches it in the context object for this turm.
        :param turn_context: The context object for this turn.
        :param force: Optional. True to bypass the cache.
        """
        if turn_context is None:
            raise TypeError("BotState.load(): turn_context cannot be None.")

        cached_state = turn_context.turn_state.get(self._context_service_key)
        storage_key = self.get_storage_key(turn_context)

        if force or not cached_state or not cached_state.state:
            items = await self._storage.read([storage_key])
            val = items.get(storage_key)
            turn_context.turn_state[self._context_service_key] = CachedBotState(val)

    async def save_changes(
        self, turn_context: TurnContext, force: bool = False
    ) -> None:
        """
        If it has changed, writes to storage the state object that is cached in the current context object
        for this turn.
        :param turn_context: The context object for this turn.
        :param force: Optional. True to save state to storage whether or not there are changes.
        """
        if turn_context is None:
            raise TypeError("BotState.save_changes(): turn_context cannot be None.")

        cached_state = turn_context.turn_state.get(self._context_service_key)

        if force or (cached_state is not None and cached_state.is_changed):
            storage_key = self.get_storage_key(turn_context)
            changes: Dict[str, object] = {storage_key: cached_state.state}
            await self._storage.write(changes)
            cached_state.hash = cached_state.compute_hash(cached_state.state)

    async def clear_state(self, turn_context: TurnContext):
        """
        Clears any state currently stored in this state scope.
        NOTE: that save_changes must be called in order for the cleared state to be persisted to the underlying store.
        :param turn_context: The context object for this turn.
        :return: None
        """
        if turn_context is None:
            raise TypeError("BotState.clear_state(): turn_context cannot be None.")

        #  Explicitly setting the hash will mean IsChanged is always true. And that will force a Save.
        cache_value = CachedBotState()
        cache_value.hash = ""
        turn_context.turn_state[self._context_service_key] = cache_value

    async def delete(self, turn_context: TurnContext) -> None:
        """
        Delete any state currently stored in this state scope.
        :param turn_context: The context object for this turn.
        :return: None
        """
        if turn_context is None:
            raise TypeError("BotState.delete(): turn_context cannot be None.")

        turn_context.turn_state.pop(self._context_service_key)

        storage_key = self.get_storage_key(turn_context)
        await self._storage.delete({storage_key})

    @abstractmethod
    def get_storage_key(self, turn_context: TurnContext) -> str:
        raise NotImplementedError()

    async def get_property_value(self, turn_context: TurnContext, property_name: str):
        if turn_context is None:
            raise TypeError(
                "BotState.get_property_value(): turn_context cannot be None."
            )
        if not property_name:
            raise TypeError(
                "BotState.get_property_value(): property_name cannot be None."
            )
        cached_state = turn_context.turn_state.get(self._context_service_key)

        # if there is no value, this will throw, to signal to IPropertyAccesor that a default value should be computed
        # This allows this to work with value types
        return cached_state.state[property_name]

    async def delete_property_value(
        self, turn_context: TurnContext, property_name: str
    ) -> None:
        """
        Deletes a property from the state cache in the turn context.
        :param turn_context: The context object for this turn.
        :param property_name: The name of the property to delete.
        :return: None
        """

        if turn_context is None:
            raise TypeError("BotState.delete_property(): turn_context cannot be None.")
        if not property_name:
            raise TypeError("BotState.delete_property(): property_name cannot be None.")
        cached_state = turn_context.turn_state.get(self._context_service_key)
        del cached_state.state[property_name]

    async def set_property_value(
        self, turn_context: TurnContext, property_name: str, value: object
    ) -> None:
        """
        Deletes a property from the state cache in the turn context.
        :param turn_context: The context object for this turn.
        :param property_name: The value to set on the property.
        :return: None
        """

        if turn_context is None:
            raise TypeError("BotState.delete_property(): turn_context cannot be None.")
        if not property_name:
            raise TypeError("BotState.delete_property(): property_name cannot be None.")
        cached_state = turn_context.turn_state.get(self._context_service_key)
        cached_state.state[property_name] = value


##
class BotStatePropertyAccessor(StatePropertyAccessor):
    def __init__(self, bot_state: BotState, name: str):
        self._bot_state = bot_state
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    async def delete(self, turn_context: TurnContext) -> None:
        await self._bot_state.load(turn_context, False)
        await self._bot_state.delete_property_value(turn_context, self._name)

    async def get(
        self,
        turn_context: TurnContext,
        default_value_or_factory: Union[Callable, object] = None,
    ) -> object:
        await self._bot_state.load(turn_context, False)
        try:
            result = await self._bot_state.get_property_value(turn_context, self._name)
            return result
        except:
            # ask for default value from factory
            if not default_value_or_factory:
                return None
            result = (
                default_value_or_factory()
                if callable(default_value_or_factory)
                else deepcopy(default_value_or_factory)
            )
            # save default value for any further calls
            await self.set(turn_context, result)
            return result

    async def set(self, turn_context: TurnContext, value: object) -> None:
        await self._bot_state.load(turn_context, False)
        await self._bot_state.set_property_value(turn_context, self._name, value)
