# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .turn_context import TurnContext
from .middleware_set import Middleware
from .storage import calculate_change_hash, StoreItem, StorageKeyFactory, Storage


class BotState(Middleware):
    def __init__(self, storage: Storage, storage_key: StorageKeyFactory):
        self.state_key = 'state'
        self.storage = storage
        self.storage_key = storage_key

    async def on_process_request(self, context, next_middleware):
        """
        Reads and writes state for your bot to storage.
        :param context:
        :param next_middleware:
        :return:
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
            key = self.storage_key(context)
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
            key = self.storage_key(context)

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
