# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest
from botbuilder.schema import Activity, ConversationReference
from botbuilder.core import TurnContext, TestAdapter
from datetime import datetime

RECEIVED_MESSAGE = Activity(type='message', text='received')
UPDATED_ACTIVITY = Activity(type='message', text='update')
DELETED_ACTIVITY_REFERENCE = ConversationReference(activity_id='1234')


class TestTestAdapter:
    @pytest.mark.asyncio
    async def test_should_call_bog_logic_when_receive_activity_is_called(self):
        async def logic(context: TurnContext):
            assert context
            assert context.activity
            assert context.activity.type == 'message'
            assert context.activity.text == 'test'
            assert context.activity.id
            assert context.activity.from_property
            assert context.activity.recipient
            assert context.activity.conversation
            assert context.activity.channel_id
            assert context.activity.service_url
        adapter = TestAdapter(logic)
        await adapter.receive_activity('test')

    @pytest.mark.asyncio
    async def test_should_support_receive_activity_with_activity(self):
        async def logic(context: TurnContext):
            assert context.activity.type == 'message'
            assert context.activity.text == 'test'
        adapter = TestAdapter(logic)
        await adapter.receive_activity(Activity(type='message', text='test'))

    @pytest.mark.asyncio
    async def test_should_set_activity_type_when_receive_activity_receives_activity_without_type(self):
        async def logic(context: TurnContext):
            assert context.activity.type == 'message'
            assert context.activity.text == 'test'
        adapter = TestAdapter(logic)
        await adapter.receive_activity(Activity(text='test'))

    @pytest.mark.asyncio
    async def test_should_support_custom_activity_id_in_receive_activity(self):
        async def logic(context: TurnContext):
            assert context.activity.id == 'myId'
            assert context.activity.type == 'message'
            assert context.activity.text == 'test'
        adapter = TestAdapter(logic)
        await adapter.receive_activity(Activity(type='message', text='test', id='myId'))

    @pytest.mark.asyncio
    async def test_should_call_bot_logic_when_send_is_called(self):
        async def logic(context: TurnContext):
                assert context.activity.text == 'test'
        adapter = TestAdapter(logic)
        await adapter.send('test')

    @pytest.mark.asyncio
    async def test_should_send_and_receive_when_test_is_called(self):
        async def logic(context: TurnContext):
            await context.send_activity(RECEIVED_MESSAGE)
        adapter = TestAdapter(logic)
        await adapter.test('test', 'received')

    @pytest.mark.asyncio
    async def test_should_send_and_throw_assertion_error_when_test_is_called(self):
        async def logic(context: TurnContext):
            await context.send_activity(RECEIVED_MESSAGE)
        adapter = TestAdapter(logic)
        try:
            await adapter.test('test', 'foobar')
        except AssertionError:
            pass
        else:
            raise AssertionError('Assertion error should have been raised')

    @pytest.mark.asyncio
    async def test_tests_should_call_test_for_each_tuple(self):
        counter = 0

        async def logic(context: TurnContext):
            nonlocal counter
            counter += 1
            await context.send_activity(Activity(type='message', text=str(counter)))

        adapter = TestAdapter(logic)
        await adapter.tests(('test', '1'), ('test', '2'), ('test', '3'))
        assert counter == 3

    @pytest.mark.asyncio
    async def test_tests_should_call_test_for_each_list(self):
        counter = 0

        async def logic(context: TurnContext):
            nonlocal counter
            counter += 1
            await context.send_activity(Activity(type='message', text=str(counter)))

        adapter = TestAdapter(logic)
        await adapter.tests(['test', '1'], ['test', '2'], ['test', '3'])
        assert counter == 3

    @pytest.mark.asyncio
    async def test_should_assert_reply_after_send(self):
        async def logic(context: TurnContext):
            await context.send_activity(RECEIVED_MESSAGE)

        adapter = TestAdapter(logic)
        test_flow = await adapter.send('test')
        await test_flow.assert_reply('received')

    @pytest.mark.asyncio
    async def test_should_support_context_update_activity_call(self):
        async def logic(context: TurnContext):
            await context.update_activity(UPDATED_ACTIVITY)
            await context.send_activity(RECEIVED_MESSAGE)

        adapter = TestAdapter(logic)
        await adapter.test('test', 'received')
        assert len(adapter.updated_activities) == 1
        assert adapter.updated_activities[0].text == UPDATED_ACTIVITY.text

    @pytest.mark.asyncio
    async def test_should_support_context_delete_activity_call(self):
        async def logic(context: TurnContext):
            await context.delete_activity(DELETED_ACTIVITY_REFERENCE)
            await context.send_activity(RECEIVED_MESSAGE)

        adapter = TestAdapter(logic)
        await adapter.test('test', 'received')
        assert len(adapter.deleted_activities) == 1
        assert adapter.deleted_activities[0].activity_id == DELETED_ACTIVITY_REFERENCE.activity_id
