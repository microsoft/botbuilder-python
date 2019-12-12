# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import uuid
from typing import List
import aiounittest

from botbuilder.core import TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import (
    Activity,
    ConversationAccount,
    ConversationReference,
    ChannelAccount,
)

from simple_adapter import SimpleAdapter
from call_counting_middleware import CallCountingMiddleware
from test_message import TestMessage


class TestBotAdapter(aiounittest.AsyncTestCase):
    def test_adapter_single_use(self):
        adapter = SimpleAdapter()
        adapter.use(CallCountingMiddleware())

    def test_adapter_use_chaining(self):
        adapter = SimpleAdapter()
        adapter.use(CallCountingMiddleware()).use(CallCountingMiddleware())

    async def test_pass_resource_responses_through(self):
        def validate_responses(  # pylint: disable=unused-argument
            activities: List[Activity],
        ):
            pass  # no need to do anything.

        adapter = SimpleAdapter(call_on_send=validate_responses)
        context = TurnContext(adapter, Activity())

        activity_id = str(uuid.uuid1())
        activity = TestMessage.message(activity_id)

        resource_response = await context.send_activity(activity)
        self.assertTrue(
            resource_response.id != activity_id, "Incorrect response Id returned"
        )

    async def test_continue_conversation_direct_msg(self):
        callback_invoked = False
        adapter = TestAdapter()
        reference = ConversationReference(
            activity_id="activityId",
            bot=ChannelAccount(id="channelId", name="testChannelAccount", role="bot"),
            channel_id="testChannel",
            service_url="testUrl",
            conversation=ConversationAccount(
                conversation_type="",
                id="testConversationId",
                is_group=False,
                name="testConversationName",
                role="user",
            ),
            user=ChannelAccount(id="channelId", name="testChannelAccount", role="bot"),
        )

        async def continue_callback(turn_context):  # pylint: disable=unused-argument
            nonlocal callback_invoked
            callback_invoked = True

        await adapter.continue_conversation(reference, continue_callback, "MyBot")
        self.assertTrue(callback_invoked)

    async def test_turn_error(self):
        async def on_error(turn_context: TurnContext, err: Exception):
            nonlocal self
            self.assertIsNotNone(turn_context, "turn_context not found.")
            self.assertIsNotNone(err, "error not found.")
            self.assertEqual(err.__class__, Exception, "unexpected error thrown.")

        adapter = SimpleAdapter()
        adapter.on_turn_error = on_error

        def handler(context: TurnContext):  # pylint: disable=unused-argument
            raise Exception

        await adapter.process_request(TestMessage.message(), handler)
