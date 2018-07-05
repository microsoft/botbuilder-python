# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest

from botbuilder.core import TurnContext, BotState, MemoryStorage, TestAdapter
from botbuilder.schema import Activity

RECEIVED_MESSAGE = Activity(type='message',
                            text='received')
STORAGE_KEY = 'stateKey'


def cached_state(context, state_key):
    cached = context.services.get(state_key)
    return cached['state'] if cached is not None else None


def key_factory(context):
    assert context is not None
    return STORAGE_KEY


class TestBotState:
    storage = MemoryStorage()
    adapter = TestAdapter()
    context = TurnContext(adapter, RECEIVED_MESSAGE)
    middleware = BotState(storage, key_factory)

    @pytest.mark.asyncio
    async def test_should_return_undefined_from_get_if_nothing_cached(self):
        state = await self.middleware.get(self.context)
        assert state is None, 'state returned'

    @pytest.mark.asyncio
    async def test_should_load_and_save_state_from_storage(self):

        async def next_middleware():
            state = cached_state(self.context, self.middleware.state_key)
            assert state is not None, 'state not loaded'
            state.test = 'foo'

        await self.middleware.on_process_request(self.context, next_middleware)
        items = await self.storage.read([STORAGE_KEY])
        assert STORAGE_KEY in items, 'saved state not found in storage.'
        assert items[STORAGE_KEY].test == 'foo', 'Missing test value in stored state.'

    @pytest.mark.skipif(True, reason='skipping while goal of test is investigated, test currently fails')
    @pytest.mark.asyncio
    async def test_should_force_read_of_state_from_storage(self):
        async def next_middleware():
            state = cached_state(self.context, self.middleware.state_key)
            assert state.test == 'foo', 'invalid initial state'
            del state.test

            # items will not have the attribute 'test'
            items = await self.middleware.read(self.context, True)
            # Similarly, the returned value from cached_state will also not have the attribute 'test'
            assert cached_state(self.context, self.middleware.state_key).test == 'foo', 'state not reloaded'

        await self.middleware.on_process_request(self.context, next_middleware)

    @pytest.mark.asyncio
    async def test_should_clear_state_storage(self):

        async def next_middleware():
            assert cached_state(self.context, self.middleware.state_key).test == 'foo', 'invalid initial state'
            await self.middleware.clear(self.context)
            cached_state_data = cached_state(self.context, self.middleware.state_key)
            assert not hasattr(cached_state_data, 'test'), 'state not cleared on context.'

        await self.middleware.on_process_request(self.context, next_middleware)
        items = await self.storage.read([STORAGE_KEY])
        assert not hasattr(items[STORAGE_KEY], 'test'), 'state not cleared from storage.'

    @pytest.mark.asyncio
    async def test_should_force_immediate_write_of_state_to_storage(self):
        async def next_middleware():
            state = cached_state(self.context, self.middleware.state_key)
            assert not hasattr(state, 'test'), 'invalid initial state'
            state.test = 'foo'

            await self.middleware.write(self.context, True)
            items = await self.storage.read([STORAGE_KEY])
            assert items[STORAGE_KEY].test == 'foo', 'state not immediately flushed.'
        await self.middleware.on_process_request(self.context, next_middleware)

    @pytest.mark.asyncio
    async def test_should_read_from_storage_if_cached_state_missing(self):
        self.context.services[self.middleware.state_key] = None
        state = await self.middleware.read(self.context)
        assert state.test == 'foo', 'state not loaded'

    @pytest.mark.asyncio
    async def test_should_read_from_cache(self):
        state = await self.middleware.read(self.context)
        assert state.test == 'foo', 'state not loaded'

    @pytest.mark.asyncio
    async def test_should_force_write_to_storage_of_an_empty_state_object(self):
        self.context.services[self.middleware.state_key] = None
        await self.middleware.write(self.context, True)

    @pytest.mark.asyncio
    async def test_should_noop_calls_to_clear_when_nothing_cached(self):
        self.context.services[self.middleware.state_key] = None
        await self.middleware.clear(self.context)
