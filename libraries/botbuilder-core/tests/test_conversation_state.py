# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest

from botbuilder.core import TurnContext, MemoryStorage, TestAdapter, ConversationState
from botbuilder.schema import Activity, ConversationAccount

RECEIVED_MESSAGE = Activity(type='message',
                            text='received',
                            channel_id='test',
                            conversation=ConversationAccount(id='convo'))
MISSING_CHANNEL_ID = Activity(type='message',
                              text='received',
                              conversation=ConversationAccount(id='convo'))
MISSING_CONVERSATION = Activity(type='message',
                                text='received',
                                channel_id='test')
END_OF_CONVERSATION = Activity(type='endOfConversation',
                               channel_id='test',
                               conversation=ConversationAccount(id='convo'))


class TestConversationState:
    storage = MemoryStorage()
    adapter = TestAdapter()
    context = TurnContext(adapter, RECEIVED_MESSAGE)
    middleware = ConversationState(storage)

    @pytest.mark.asyncio
    async def test_should_load_and_save_state_from_storage(self):
        key = None

        async def next_middleware():
            nonlocal key
            key = self.middleware.get_storage_key(self.context)
            state = await self.middleware.get(self.context)
            assert state is not None, 'State not loaded'
            assert key is not None, 'Key not found'
            state.test = 'foo'

        await self.middleware.on_process_request(self.context, next_middleware)

        items = await self.storage.read([key])
        assert key in items, 'Saved state not found in storage.'
        assert items[key].test == 'foo', 'Missing test value in stored state.'

    @pytest.mark.asyncio
    async def test_should_ignore_any_activities_that_are_not_endOfConversation(self):
        key = None

        async def next_middleware():
            nonlocal key
            key = self.middleware.get_storage_key(self.context)
            state = await self.middleware.get(self.context)
            assert state.test == 'foo', 'invalid initial state'
            await self.context.send_activity(Activity(type='message', text='foo'))

        await self.middleware.on_process_request(self.context, next_middleware)
        items = await self.storage.read([key])
        assert hasattr(items[key], 'test'), 'state cleared and should not have been'

    @pytest.mark.asyncio
    async def test_should_reject_with_error_if_channel_id_is_missing(self):
        context = TurnContext(self.adapter, MISSING_CHANNEL_ID)

        async def next_middleware():
            assert False, 'should not have called next_middleware'

        try:
            await self.middleware.on_process_request(context, next_middleware)
        except AttributeError:
            pass
        except Exception as e:
            raise e
        else:
            raise AssertionError('Should not have completed and not raised AttributeError.')

    @pytest.mark.asyncio
    async def test_should_reject_with_error_if_conversation_is_missing(self):
        context = TurnContext(self.adapter, MISSING_CONVERSATION)

        async def next_middleware():
            assert False, 'should not have called next_middleware'

        try:
            await self.middleware.on_process_request(context, next_middleware)
        except AttributeError:
            pass
        except Exception as e:
            raise e
        else:
            raise AssertionError('Should not have completed and not raised AttributeError.')
