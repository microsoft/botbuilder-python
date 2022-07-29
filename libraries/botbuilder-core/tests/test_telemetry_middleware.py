# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# pylint: disable=line-too-long,missing-docstring,unused-variable
import copy
import uuid
from typing import Dict
from unittest.mock import Mock
import aiounittest
from botframework.connector import Channels

from botbuilder.core import (
    NullTelemetryClient,
    TelemetryLoggerMiddleware,
    TelemetryLoggerConstants,
    TurnContext,
    MessageFactory,
)
from botbuilder.core.adapters import TestAdapter, TestFlow
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    ConversationAccount,
    ConversationReference,
)
from botbuilder.schema.teams import TeamInfo, TeamsChannelData, TenantInfo


class TestTelemetryMiddleware(aiounittest.AsyncTestCase):
    # pylint: disable=unused-argument
    async def test_create_middleware(self):
        telemetry = NullTelemetryClient()
        my_logger = TelemetryLoggerMiddleware(telemetry, True)
        assert my_logger

    async def test_do_not_throw_on_null_from(self):
        telemetry = Mock()
        my_logger = TelemetryLoggerMiddleware(telemetry, False)

        adapter = TestAdapter(
            template_or_conversation=Activity(
                channel_id="test",
                recipient=ChannelAccount(id="bot", name="Bot"),
                conversation=ConversationAccount(id=str(uuid.uuid4())),
            )
        )
        adapter.use(my_logger)

        async def send_proactive(context: TurnContext):
            await context.send_activity("proactive")

        async def logic(context: TurnContext):
            await adapter.create_conversation(
                context.activity.channel_id,
                send_proactive,
            )

        adapter.logic = logic

        test_flow = TestFlow(None, adapter)
        await test_flow.send("foo")
        await test_flow.assert_reply("proactive")

        telemetry_calls = [
            (
                TelemetryLoggerConstants.BOT_MSG_RECEIVE_EVENT,
                {
                    "fromId": None,
                    "conversationName": None,
                    "locale": None,
                    "recipientId": "bot",
                    "recipientName": "Bot",
                },
            ),
        ]
        self.assert_telemetry_calls(telemetry, telemetry_calls)

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
                    "recipientName": "Bot",
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
                    "recipientName": "Bot",
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
                    "recipientName": "Bot",
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
                    "recipientName": "Bot",
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

    async def test_log_teams(self):
        telemetry = Mock()
        my_logger = TelemetryLoggerMiddleware(telemetry, True)

        adapter = TestAdapter(
            template_or_conversation=ConversationReference(channel_id=Channels.ms_teams)
        )
        adapter.use(my_logger)

        team_info = TeamInfo(
            id="teamId",
            name="teamName",
        )

        channel_data = TeamsChannelData(
            team=team_info,
            tenant=TenantInfo(id="tenantId"),
        ).serialize()

        activity = MessageFactory.text("test")
        activity.channel_data = channel_data
        activity.from_property = ChannelAccount(
            id="userId",
            name="userName",
            aad_object_id="aaId",
        )

        test_flow = TestFlow(None, adapter)
        await test_flow.send(activity)

        telemetry_call_expected = [
            (
                TelemetryLoggerConstants.BOT_MSG_RECEIVE_EVENT,
                {
                    "text": "test",
                    "fromId": "userId",
                    "recipientId": "bot",
                    "recipientName": "Bot",
                    "TeamsTenantId": "tenantId",
                    "TeamsUserAadObjectId": "aaId",
                    "TeamsTeamInfo": TeamInfo.serialize(team_info),
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
