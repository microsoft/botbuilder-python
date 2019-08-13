# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# pylint: disable=line-too-long,missing-docstring,unused-variable
import copy
from typing import Dict
from unittest.mock import Mock
import aiounittest
from botbuilder.core import (
    NullTelemetryClient,
    TelemetryLoggerMiddleware,
    TelemetryLoggerConstants,
    TurnContext,
)
from botbuilder.core.adapters import TestAdapter, TestFlow
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    ConversationAccount,
)


class TestTelemetryMiddleware(aiounittest.AsyncTestCase):
    # pylint: disable=unused-argument
    async def test_create_middleware(self):
        telemetry = NullTelemetryClient()
        my_logger = TelemetryLoggerMiddleware(telemetry, True)
        assert my_logger

    async def test_should_send_receive(self):
        telemetry = Mock()
        my_logger = TelemetryLoggerMiddleware(telemetry, True)

        async def logic(context: TurnContext):
            await context.send_activity(f"echo:{context.activity.text}")

        adapter = TestAdapter(logic)
        adapter.use(my_logger)
        test_flow = TestFlow(None, adapter)
        test_flow = await test_flow.send("foo")
        test_flow = await test_flow.assert_reply("echo:foo")
        test_flow = await test_flow.send("bar")
        await test_flow.assert_reply("echo:bar")

        # assert
        # Note: None values just check for existence of the key, not the explicit
        #     value (generated)
        telemetry_calls = [
            (
                TelemetryLoggerConstants.BOT_MSG_RECEIVE_EVENT,
                {
                    "text": "foo",
                    "fromId": "User1",
                    "conversationName": None,
                    "locale": None,
                    "recipientId": "bot",
                    "recipientName": "user",
                },
            ),
            (
                TelemetryLoggerConstants.BOT_MSG_SEND_EVENT,
                {
                    "text": "echo:foo",
                    "replyActivityId": None,
                    "recipientId": None,
                    "conversationName": None,
                    "locale": None,
                },
            ),
            (
                TelemetryLoggerConstants.BOT_MSG_RECEIVE_EVENT,
                {
                    "text": "bar",
                    "fromId": "User1",
                    "conversationName": None,
                    "locale": None,
                    "recipientId": "bot",
                    "recipientName": "user",
                    "fromName": "user",
                },
            ),
            (
                TelemetryLoggerConstants.BOT_MSG_SEND_EVENT,
                {
                    "replyActivityId": None,
                    "recipientId": "User1",
                    "conversationName": None,
                    "locale": None,
                    "fromName": "Bot",
                    "text": "echo:bar",
                },
            ),
        ]
        self.assert_telemetry_calls(telemetry, telemetry_calls)

    async def test_none_telemetry_client(self):
        my_logger = TelemetryLoggerMiddleware(None, True)

        async def logic(context: TurnContext):
            await context.send_activity(f"echo:{context.activity.text}")

        adapter = TestAdapter(logic)
        adapter.use(my_logger)
        test_flow = TestFlow(None, adapter)
        test_flow = await test_flow.send("foo")
        test_flow = await test_flow.assert_reply("echo:foo")
        test_flow = await test_flow.send("bar")
        await test_flow.assert_reply("echo:bar")

    async def test_log_update(self):
        telemetry = Mock()
        my_logger = TelemetryLoggerMiddleware(telemetry, True)
        activity_to_update = None

        async def process(context: TurnContext) -> None:
            nonlocal activity_to_update
            if context.activity.text == "update":
                if not activity_to_update:
                    raise Exception("activity to update not set yet!")
                activity_to_update.text = "new response"
                await context.update_activity(activity_to_update)
            else:
                activity = self.create_reply(context.activity, "response")
                response = await context.send_activity(activity)
                activity.id = response.id
                # clone the activity, so we can use it to do an update
                activity_to_update = copy.copy(activity)
                # await context.send_activity(f'echo:{context.activity.text}')

        adapter = TestAdapter(process)
        adapter.use(my_logger)
        test_flow = TestFlow(None, adapter)
        test_flow = await test_flow.send("foo")
        test_flow = await test_flow.assert_reply("response")
        test_flow = await test_flow.send("update")

        # assert
        # Note: None values just check for existence of the key, not the explicit
        #     value (generated)
        telemetry_call_expected = [
            (
                TelemetryLoggerConstants.BOT_MSG_RECEIVE_EVENT,
                {
                    "text": "foo",
                    "fromId": "User1",
                    "conversationName": None,
                    "locale": None,
                    "recipientId": "bot",
                    "recipientName": "user",
                },
            ),
            (
                TelemetryLoggerConstants.BOT_MSG_SEND_EVENT,
                {
                    "replyActivityId": "1",
                    "recipientId": "User1",
                    "conversationName": None,
                    "locale": None,
                    "fromName": "Bot",
                    "text": "response",
                },
            ),
            (
                TelemetryLoggerConstants.BOT_MSG_RECEIVE_EVENT,
                {
                    "text": "update",
                    "fromId": "User1",
                    "conversationName": None,
                    "locale": None,
                    "recipientId": "bot",
                    "recipientName": "user",
                    "fromName": "user",
                },
            ),
            (
                TelemetryLoggerConstants.BOT_MSG_UPDATE_EVENT,
                {
                    "recipientId": "User1",
                    "conversationId": "Convo1",
                    "conversationName": None,
                    "locale": None,
                    "text": "new response",
                },
            ),
        ]
        self.assert_telemetry_calls(telemetry, telemetry_call_expected)

    def create_reply(self, activity, text, locale=None):
        return Activity(
            type=ActivityTypes.message,
            from_property=ChannelAccount(
                id=activity.recipient.id, name=activity.recipient.name
            ),
            recipient=ChannelAccount(
                id=activity.from_property.id, name=activity.from_property.name
            ),
            reply_to_id=activity.id,
            service_url=activity.service_url,
            channel_id=activity.channel_id,
            conversation=ConversationAccount(
                is_group=activity.conversation.is_group,
                id=activity.conversation.id,
                name=activity.conversation.name,
            ),
            text=text or "",
            locale=locale or activity.locale,
        )

    def assert_telemetry_call(
        self, telemetry_mock, index: int, event_name: str, props: Dict[str, str]
    ) -> None:
        self.assertTrue(
            index < len(telemetry_mock.track_event.call_args_list),
            f"{len(telemetry_mock.track_event.call_args_list)} calls were made. You were asking for index {index}.",
        )
        args, kwargs = telemetry_mock.track_event.call_args_list[index]
        self.assertEqual(
            args[0],
            event_name,
            f"Event NAME not matching.\n   Expected: {props}\n   Generated: {args[1]}",
        )

        for key, val in props.items():
            self.assertTrue(
                key in args[1],
                msg=f"Could not find value {key} in '{args[1]}' for index {index}",
            )
            self.assertTrue(
                isinstance(args[1], dict),
                f"ERROR: Second parm passed not a dictionary! {type(args[1])}",
            )
            if props[key]:
                self.assertTrue(
                    val == args[1][key],
                    f'   ERROR: Validate failed: "{val}" expected, "{args[1][key]}" generated',
                )

    def assert_telemetry_calls(self, telemetry_mock, calls) -> None:
        index = 0
        for event_name, props in calls:
            self.assert_telemetry_call(telemetry_mock, index, event_name, props)
            index += 1
        if index != len(telemetry_mock.track_event.call_args_list):
            self.assertTrue(  # pylint: disable=redundant-unittest-assert
                False,
                f"Found {len(telemetry_mock.track_event.call_args_list)} calls, testing for {index + 1}",
            )
