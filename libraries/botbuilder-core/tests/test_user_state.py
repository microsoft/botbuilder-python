# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest

from botbuilder.core import TurnContext, MemoryStorage, StoreItem, TestAdapter, UserState
from botbuilder.schema import Activity, ChannelAccount

RECEIVED_MESSAGE = Activity(type='message',
                            text='received',
                            channel_id='test',
                            from_property=ChannelAccount(id='user'))
MISSING_CHANNEL_ID = Activity(type='message',
                              text='received',
                              from_property=ChannelAccount(id='user'))
MISSING_FROM_PROPERTY = Activity(type='message',
                                 text='received',
                                 channel_id='test')


class TestUserState:
    storage = MemoryStorage()
    adapter = TestAdapter()
    context = TurnContext(adapter, RECEIVED_MESSAGE)
    middleware = UserState(storage)

    @pytest.mark.asyncio
    async def test_should_load_and_save_state_from_storage(self):

        async def next_middleware():
            state = await self.middleware.get(self.context)
            assert isinstance(state, StoreItem), 'State not loaded'
            state.test = 'foo'

        await self.middleware.on_process_request(self.context, next_middleware)
        key = self.middleware.get_storage_key(self.context)
        assert type(key) == str, 'Key not found'
        items = await self.storage.read([key])
        assert key in items, 'Saved state not found in storage'
        assert items[key].test == 'foo', 'Missing test value in stored state.'

    @pytest.mark.asyncio
    async def test_should_reject_with_error_if_channel_id_is_missing(self):
        context = TurnContext(self.adapter, MISSING_CHANNEL_ID)

        async def next_middleware():
            assert False, 'Should not have called next_middleware'

        try:
            await self.middleware.on_process_request(context, next_middleware)
        except AttributeError:
            pass
        else:
            raise AssertionError('Should not have completed and not raised AttributeError.')

    @pytest.mark.asyncio
    async def test_should_reject_with_error_if_from_property_is_missing(self):
        context = TurnContext(self.adapter, MISSING_FROM_PROPERTY)

        async def next_middleware():
            assert False, 'Should not have called next_middleware'

        try:
            await self.middleware.on_process_request(context, next_middleware)
        except AttributeError:
            pass
        else:
            raise AssertionError('Should not have completed and not raised AttributeError.')
