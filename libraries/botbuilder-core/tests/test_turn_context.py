# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest

from botbuilder.schema import Activity, ChannelAccount, ResourceResponse, ConversationAccount
from botbuilder.core import BotAdapter, TurnContext
ACTIVITY = Activity(id='1234',
                    type='message',
                    text='test',
                    from_property=ChannelAccount(id='user', name='User Name'),
                    recipient=ChannelAccount(id='bot', name='Bot Name'),
                    conversation=ConversationAccount(id='convo', name='Convo Name'),
                    channel_id='UnitTest',
                    service_url='https://example.org'
                    )


class SimpleAdapter(BotAdapter):
    async def send_activities(self, context, activities):
        responses = []
        assert context is not None
        assert activities is not None
        assert type(activities) == list
        assert len(activities) > 0
        for (idx, activity) in enumerate(activities):
            assert isinstance(activity, Activity)
            assert activity.type == 'message'
            responses.append(ResourceResponse(id='5678'))
        return responses

    async def update_activity(self, context, activity):
        assert context is not None
        assert activity is not None

    async def delete_activity(self, context, reference):
        assert context is not None
        assert reference is not None
        assert reference.activity_id == '1234'


class TestBotContext:
    def test_should_create_context_with_request_and_adapter(self):
        context = TurnContext(SimpleAdapter(), ACTIVITY)

    def test_should_not_create_context_without_request(self):
        try:
            context = TurnContext(SimpleAdapter(), None)
        except TypeError:
            pass
        except Exception as e:
            raise e

    def test_should_not_create_context_without_adapter(self):
        try:
            context = TurnContext(None, ACTIVITY)
        except TypeError:
            pass
        except Exception as e:
            raise e

    def test_should_create_context_with_older_context(self):
        context = TurnContext(SimpleAdapter(), ACTIVITY)
        new_context = TurnContext(context)

    def test_copy_to_should_copy_all_references(self):
        old_adapter = SimpleAdapter()
        old_activity = Activity(id='2', type='message', text='test copy')
        old_context = TurnContext(old_adapter, old_activity)
        old_context.responded = True

        async def send_activities_handler(context, activities, next_handler):
            assert context is not None
            assert activities is not None
            assert next_handler is not None
            await next_handler

        async def delete_activity_handler(context, reference, next_handler):
            assert context is not None
            assert reference is not None
            assert next_handler is not None
            await next_handler

        async def update_activity_handler(context, activity, next_handler):
            assert context is not None
            assert activity is not None
            assert next_handler is not None
            await next_handler

        old_context.on_send_activities(send_activities_handler)
        old_context.on_delete_activity(delete_activity_handler)
        old_context.on_update_activity(update_activity_handler)

        adapter = SimpleAdapter()
        new_context = TurnContext(adapter, ACTIVITY)
        assert len(new_context._on_send_activities) == 0
        assert len(new_context._on_update_activity) == 0
        assert len(new_context._on_delete_activity) == 0

        old_context.copy_to(new_context)

        assert new_context.adapter == old_adapter
        assert new_context.activity == old_activity
        assert new_context.responded is True
        assert len(new_context._on_send_activities) == 1
        assert len(new_context._on_update_activity) == 1
        assert len(new_context._on_delete_activity) == 1

    def test_responded_should_be_automatically_set_to_False(self):
        context = TurnContext(SimpleAdapter(), ACTIVITY)
        assert context.responded is False

    def test_should_be_able_to_set_responded_to_True(self):
        context = TurnContext(SimpleAdapter(), ACTIVITY)
        assert context.responded is False
        context.responded = True
        assert context.responded

    def test_should_not_be_able_to_set_responded_to_False(self):
        context = TurnContext(SimpleAdapter(), ACTIVITY)
        try:
            context.responded = False
        except ValueError:
            pass
        except Exception as e:
            raise e

    @pytest.mark.asyncio
    async def test_should_call_on_delete_activity_handlers_before_deletion(self):
        context = TurnContext(SimpleAdapter(), ACTIVITY)
        called = False

        async def delete_handler(context, reference, next_handler_coroutine):
            nonlocal called
            called = True
            assert reference is not None
            assert context is not None
            assert reference.activity_id == '1234'
            await next_handler_coroutine()

        context.on_delete_activity(delete_handler)
        await context.delete_activity(ACTIVITY.id)
        assert called is True

    @pytest.mark.asyncio
    async def test_should_call_multiple_on_delete_activity_handlers_in_order(self):
        context = TurnContext(SimpleAdapter(), ACTIVITY)
        called_first = False
        called_second = False

        async def first_delete_handler(context, reference, next_handler_coroutine):
            nonlocal called_first, called_second
            assert called_first is False, 'called_first should not be True before first_delete_handler is called.'
            called_first = True
            assert called_second is False, 'Second on_delete_activity handler was called before first.'
            assert reference is not None
            assert context is not None
            assert reference.activity_id == '1234'
            await next_handler_coroutine()

        async def second_delete_handler(context, reference, next_handler_coroutine):
            nonlocal called_first, called_second
            assert called_first
            assert called_second is False, 'called_second was set to True before second handler was called.'
            called_second = True
            assert reference is not None
            assert context is not None
            assert reference.activity_id == '1234'
            await next_handler_coroutine()

        context.on_delete_activity(first_delete_handler)
        context.on_delete_activity(second_delete_handler)
        await context.delete_activity(ACTIVITY.id)
        assert called_first is True
        assert called_second is True

    @pytest.mark.asyncio
    async def test_should_call_send_on_activities_handler_before_send(self):
        context = TurnContext(SimpleAdapter(), ACTIVITY)
        called = False

        async def send_handler(context, activities, next_handler_coroutine):
            nonlocal called
            called = True
            assert activities is not None
            assert context is not None
            assert activities[0].id == '1234'
            await next_handler_coroutine()

        context.on_send_activities(send_handler)
        await context.send_activity(ACTIVITY)
        assert called is True

    @pytest.mark.asyncio
    async def test_should_call_on_update_activity_handler_before_update(self):
        context = TurnContext(SimpleAdapter(), ACTIVITY)
        called = False

        async def update_handler(context, activity, next_handler_coroutine):
            nonlocal called
            called = True
            assert activity is not None
            assert context is not None
            assert activity.id == '1234'
            await next_handler_coroutine()

        context.on_update_activity(update_handler)
        await context.update_activity(ACTIVITY)
        assert called is True

    def test_get_conversation_reference_should_return_valid_reference(self):
        reference = TurnContext.get_conversation_reference(ACTIVITY)

        assert reference.activity_id == ACTIVITY.id
        assert reference.user == ACTIVITY.from_property
        assert reference.bot == ACTIVITY.recipient
        assert reference.conversation == ACTIVITY.conversation
        assert reference.channel_id == ACTIVITY.channel_id
        assert reference.service_url == ACTIVITY.service_url

    def test_apply_conversation_reference_should_return_prepare_reply_when_is_incoming_is_False(self):
        reference = TurnContext.get_conversation_reference(ACTIVITY)
        reply = TurnContext.apply_conversation_reference(Activity(type='message', text='reply'), reference)

        assert reply.recipient == ACTIVITY.from_property
        assert reply.from_property == ACTIVITY.recipient
        assert reply.conversation == ACTIVITY.conversation
        assert reply.service_url == ACTIVITY.service_url
        assert reply.channel_id == ACTIVITY.channel_id

    def test_apply_conversation_reference_when_is_incoming_is_True_should_not_prepare_a_reply(self):
        reference = TurnContext.get_conversation_reference(ACTIVITY)
        reply = TurnContext.apply_conversation_reference(Activity(type='message', text='reply'), reference, True)

        assert reply.recipient == ACTIVITY.recipient
        assert reply.from_property == ACTIVITY.from_property
        assert reply.conversation == ACTIVITY.conversation
        assert reply.service_url == ACTIVITY.service_url
        assert reply.channel_id == ACTIVITY.channel_id