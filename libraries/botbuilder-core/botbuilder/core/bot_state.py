# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .turn_context import TurnContext
from .middleware_set import Middleware
from .storage import calculate_change_hash, StoreItem, StorageKeyFactory, Storage
from .property_manager import PropertyManager
from botbuilder.core.state_property_accessor import StatePropertyAccessor
from botbuilder.core import turn_context
from _ast import Try


class BotState(PropertyManager):
    def __init__(self, storage: Storage, context_service_key: str):
        self.state_key = 'state'
        self.storage = storage
        self._context_storage_key = context_service_key
        
          

    def create_property(self, name:str) -> StatePropertyAccessor:
        """Create a property definition and register it with this BotState.
        Parameters
        ----------
        name
            The name of the property.
           
        Returns
        -------
        StatePropertyAccessor
            If successful, the state property accessor created.
        """
        if not name:
            raise TypeError('BotState.create_property(): BotState cannot be None.')
        return BotStatePropertyAccessor(self, name);


    async def load(self, turn_context: TurnContext, force: bool = False):
        """Reads in  the current state object and caches it in the context object for this turm.
        Parameters
        ----------
        turn_context
            The context object for this turn.
        force
            Optional. True to bypass the cache.
        """
        if not turn_context:
            raise TypeError('BotState.load(): turn_context cannot be None.')
        cached_state = turn_context.turn_state.get(self._context_storage_key)
        storage_key = get_storage_key(turn_context)
        if (force or not cached_state or not cached_state.state) :
            items = await _storage.read([storage_key])
            val = items.get(storage_key)
            turn_context.turn_state[self._context_storage_key] = CachedBotState(val)
        
    async def on_process_request(self, context, next_middleware):
        """Reads and writes state for your bot to storage.
        Parameters
        ----------
        context
            The Turn Context.
        next_middleware
            The next middleware component
            
        Returns
        -------
        """
        await self.read(context, True)
        # For libraries like aiohttp, the web.Response need to be bubbled up from the process_activity logic, which is
        # the results are stored from next_middleware()
        logic_results = await next_middleware()

        await self.write(context)
        return logic_results

    async def read(self, context: TurnContext, force: bool=False):
        """
        Reads in and caches the current state object for a turn.
        :param context:
        :param force:
        :return:
        """
        cached = context.services.get(self.state_key)

        if force or cached is None or ('state' in cached and cached['state'] is None):
            key = self._context_storage_key(context)
            items = await self.storage.read([key])
            state = items.get(key, StoreItem())
            hash_state = calculate_change_hash(state)

            context.services[self.state_key] = {'state': state, 'hash': hash_state}
            return state

        return cached['state']

    async def write(self, context: TurnContext, force: bool=False):
        """
        Saves the cached state object if it's been changed.
        :param context:
        :param force:
        :return:
        """
        cached = context.services.get(self.state_key)

        if force or (cached is not None and cached.get('hash', None) != calculate_change_hash(cached['state'])):
            key = self._context_storage_key(context)

            if cached is None:
                cached = {'state': StoreItem(e_tag='*'), 'hash': ''}
            changes = {key: cached['state']}
            await self.storage.write(changes)

            cached['hash'] = calculate_change_hash(cached['state'])
            context.services[self.state_key] = cached

    async def clear(self, context: TurnContext):
        """
        Clears the current state object for a turn.
        :param context:
        :return:
        """
        cached = context.services.get(self.state_key)
        if cached is not None:
            cached['state'] = StoreItem()
            context.services[self.state_key] = cached

    async def get(self, context: TurnContext):
        """
        Returns a cached state object or undefined if not cached.
        :param context:
        :return:
        """
        cached = context.services.get(self.state_key)
        state = None
        if isinstance(cached, dict) and isinstance(cached['state'], StoreItem):
            state = cached['state']
        return state


class BotStatePropertyAccessor(StatePropertyAccessor):
    def __init__(self, bot_state: BotState, name: str):
        self._bot_state = bot_state
        self._name = name
        
    @property
    def name(self) -> str:
        return _name;
    
    async def delete(self, turn_context: TurnContext):
        await self._bot_state.load(turn_context, False)
        await self._bot_state.delete_property_value(turn_context, name)
        
    async def get(self, turn_context: TurnContext, default_value_factory):
        await self._bot_state.load(turn_context, false)
        try:
            return await _bot_state.get_property_value(turn_context, name)
        except:
            # ask for default value from factory
            if not default_value_factory:
                return None
            result = default_value_factory()
            # save default value for any further calls
            await set(turn_context, result)
            return result
        
    async def set(self, turn_context: TurnContext, value):
        await _bot_state.load(turn_context, false)
        await _bot_state.set_property_value(turn_context, name)
