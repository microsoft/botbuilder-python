# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest


from botbuilder.core import TurnContext, MessageFactory
from botbuilder.core.teams import TeamsInfo, TeamsActivityHandler
from botbuilder.schema import Activity
from botbuilder.schema.teams import TeamsChannelData, TeamInfo
from botframework.connector import Channels
from simple_adapter_with_create_conversation import SimpleAdapterWithCreateConversation


class TestTeamsInfo(aiounittest.AsyncTestCase):
    async def test_send_message_to_teams(self):
        def create_conversation():
            pass

        adapter = SimpleAdapterWithCreateConversation(
            call_create_conversation=create_conversation
        )

        activity = Activity(
            type="message",
            text="test_send_message_to_teams_channel",
            channel_id=Channels.ms_teams,
            service_url="https://example.org",
            channel_data=TeamsChannelData(team=TeamInfo(id="team-id")),
        )
        turn_context = TurnContext(adapter, activity)
        handler = TestTeamsActivityHandler()
        await handler.on_turn(turn_context)


class TestTeamsActivityHandler(TeamsActivityHandler):
    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        if turn_context.activity.text == "test_send_message_to_teams_channel":
            await self.call_send_message_to_teams(turn_context)

    async def call_send_message_to_teams(self, turn_context: TurnContext):
        msg = MessageFactory.text("call_send_message_to_teams")
        channel_id = "teams_channel_123"
        reference = await TeamsInfo.send_message_to_teams_channel(
            turn_context, msg, channel_id
        )

        assert reference[0].activity_id == "new_conversation_id"
        assert reference[1] == "reference123"
