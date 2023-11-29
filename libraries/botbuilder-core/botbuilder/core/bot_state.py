# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import abstractmethod
from copy import deepcopy
from typing import Callable, Dict, Union
from jsonpickle.pickler import Pickler
from botbuilder.core.state_property_accessor import StatePropertyAccessor
from .bot_assert import BotAssert
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
    """
    Defines a state management object and automates the reading and writing of
    associated state properties to a storage layer.

    .. remarks::
        Each state management object defines a scope for a storage layer.
        State properties are created within a state management scope, and the Bot Framework
        defines these scopes: :class:`ConversationState`, :class:`UserState`, and :class:`PrivateConversationState`.
        You can define additional scopes for your bot.
    """

    def __init__(self, storage: Storage, context_service_key: str):
        """
        Initializes a new instance of the :class:`BotState` class.

        :param storage: The storage layer this state management object will use to store and retrieve state
        :type storage:  :class:`bptbuilder.core.Storage`
        :param context_service_key: The key for the state cache for this :class:`BotState`
        :type context_service_key: str

        .. remarks::
            This constructor creates a state management object and associated scope. The object uses
            the :param storage: to persist state property values and the :param context_service_key: to cache state
            within the context for each turn.

        :raises: It raises an argument null exception.
        """
        self.state_key = "state"
        self._storage = storage
        self._context_service_key = context_service_key

    def get_cached_state(self, turn_context: TurnContext):
        """
        Gets the cached bot state instance that wraps the raw cached data for this "BotState"
        from the turn context.

        :param turn_context: The context object for this turn.
        :type turn_context: :class:`TurnContext`
        :return: The cached bot state instance.
        """
        BotAssert.context_not_none(turn_context)
        return turn_context.turn_state.get(self._context_service_key)

    def create_property(self, name: str) -> StatePropertyAccessor:
        """
        Creates a property definition and registers it with this :class:`BotState`.

        :param name: The name of the property
        :type name: str
        :return: If successful, the state property accessor created
        :rtype: :class:`StatePropertyAccessor`
        """
        if not name:
            raise TypeError("BotState.create_property(): name cannot be None or empty.")
        return BotStatePropertyAccessor(self, name)

    def get(self, turn_context: TurnContext) -> Dict[str, object]:
        BotAssert.context_not_none(turn_context)
        cached = self.get_cached_state(turn_context)

        return getattr(cached, "state", None)

    async def load(self, turn_context: TurnContext, force: bool = False) -> None:
        """
        Reads the current state object and caches it in the context object for this turn.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`TurnContext`
        :param force: Optional, true to bypass the cache
        :type force: bool
        """
        BotAssert.context_not_none(turn_context)

        cached_state = self.get_cached_state(turn_context)
        storage_key = self.get_storage_key(turn_context)

        if force or not cached_state or not cached_state.state:
            items = await self._storage.read([storage_key])
            val = items.get(storage_key)
            turn_context.turn_state[self._context_service_key] = CachedBotState(val)

    async def save_changes(
        self, turn_context: TurnContext, force: bool = False
    ) -> None:
        """
        Saves the state cached in the current context for this turn.
        If the state has changed, it saves the state cached in the current context for this turn.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`TurnContext`
        :param force: Optional, true to save state to storage whether or not there are changes
        :type force: bool
        """
        BotAssert.context_not_none(turn_context)

        cached_state = self.get_cached_state(turn_context)

        if force or (cached_state is not None and cached_state.is_changed):
            storage_key = self.get_storage_key(turn_context)
            changes: Dict[str, object] = {storage_key: cached_state.state}
            await self._storage.write(changes)
            cached_state.hash = cached_state.compute_hash(cached_state.state)

    async def clear_state(self, turn_context: TurnContext):
        """
        Clears any state currently stored in this state scope.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`TurnContext`

        :return: None

        .. remarks::
            This function must be called in order for the cleared state to be persisted to the underlying store.
        """
        BotAssert.context_not_none(turn_context)

        #  Explicitly setting the hash will mean IsChanged is always true. And that will force a Save.
        cache_value = CachedBotState()
        cache_value.hash = ""
        turn_context.turn_state[self._context_service_key] = cache_value

    async def delete(self, turn_context: TurnContext) -> None:
        """
        Deletes any state currently stored in this state scope.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`TurnContext`

        :return: None
        """
        BotAssert.context_not_none(turn_context)

        turn_context.turn_state.pop(self._context_service_key)

        storage_key = self.get_storage_key(turn_context)
        await self._storage.delete({storage_key})

    @abstractmethod
    def get_storage_key(self, turn_context: TurnContext) -> str:
        raise NotImplementedError()

    async def get_property_value(self, turn_context: TurnContext, property_name: str):
        """
        Gets the value of the specified property in the turn context.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`TurnContext`
        :param property_name: The property name
        :type property_name: str

        :return: The value of the property
        """
        BotAssert.context_not_none(turn_context)
        if not property_name:
            raise TypeError(
                "BotState.get_property_value(): property_name cannot be None."
            )
        cached_state = self.get_cached_state(turn_context)

        # if there is no value, this will throw, to signal to IPropertyAccesor that a default value should be computed
        # This allows this to work with value types
        return cached_state.state[property_name]

    async def delete_property_value(
        self, turn_context: TurnContext, property_name: str
    ) -> None:
        """
        Deletes a property from the state cache in the turn context.

        :param turn_context: The context object for this turn
        :type turn_context: :TurnContext`
        :param property_name: The name of the property to delete
        :type property_name: str

        :return: None
        """
        BotAssert.context_not_none(turn_context)
        if not property_name:
            raise TypeError("BotState.delete_property(): property_name cannot be None.")
        cached_state = self.get_cached_state(turn_context)
        del cached_state.state[property_name]

    async def set_property_value(
        self, turn_context: TurnContext, property_name: str, value: object
    ) -> None:
        """
        Sets a property to the specified value in the turn context.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`TurnContext`
        :param property_name: The property name
        :type property_name: str
        :param value: The value to assign to the property
        :type value: Object

        :return: None
        """
        BotAssert.context_not_none(turn_context)
        if not property_name:
            raise TypeError("BotState.delete_property(): property_name cannot be None.")
        cached_state = self.get_cached_state(turn_context)
        cached_state.state[property_name] = value


class BotStatePropertyAccessor(StatePropertyAccessor):
    """
    Defines methods for accessing a state property created in a :class:`BotState` object.
    """

    def __init__(self, bot_state: BotState, name: str):
        """
        Initializes a new instance of the :class:`BotStatePropertyAccessor` class.

        :param bot_state: The state object to access
        :type bot_state:  :class:`BotState`
        :param name: The name of the state property to access
        :type name: str

        """
        self._bot_state = bot_state
        self._name = name

    @property
    def name(self) -> str:
        """
        The name of the property.
        """
        return self._name

    async def delete(self, turn_context: TurnContext) -> None:
        """
        Deletes the property.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`TurnContext`
        """
        await self._bot_state.load(turn_context, False)
        await self._bot_state.delete_property_value(turn_context, self._name)

    async def get(
        self,
        turn_context: TurnContext,
        default_value_or_factory: Union[Callable, object] = None,
    ) -> object:
        """
        Gets the property value.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`TurnContext`
        :param default_value_or_factory: Defines the default value for the property
        """
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
        """
        Sets the property value.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`TurnContext`

        :param value: The value to assign to the property
        """
        await self._bot_state.load(turn_context, False)
        await self._bot_state.set_property_value(turn_context, self._name, value)
