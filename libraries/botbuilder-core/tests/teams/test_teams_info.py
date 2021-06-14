# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botframework.connector import Channels

from botbuilder.core import TurnContext, MessageFactory
from botbuilder.core.teams import TeamsInfo, TeamsActivityHandler
from botbuilder.schema import (
    Activity,
    ChannelAccount,
    ConversationAccount,
)
from simple_adapter_with_create_conversation import SimpleAdapterWithCreateConversation

ACTIVITY = Activity(
    id="1234",
    type="message",
    text="test",
    from_property=ChannelAccount(id="user", name="User Name"),
    recipient=ChannelAccount(id="bot", name="Bot Name"),
    conversation=ConversationAccount(id="convo", name="Convo Name"),
    channel_data={"channelData": {}},
    channel_id="UnitTest",
    locale="en-us",
    service_url="https://example.org",
)


class TestTeamsInfo(aiounittest.AsyncTestCase):
    async def test_send_message_to_teams_channels_without_activity(self):
        def create_conversation():
            pass

        adapter = SimpleAdapterWithCreateConversation(
            call_create_conversation=create_conversation
        )

        activity = Activity()
        turn_context = TurnContext(adapter, activity)

        try:
            await TeamsInfo.send_message_to_teams_channel(
                turn_context, None, "channelId123"
            )
        except ValueError:
            pass
        else:
            assert False, "should have raise ValueError"

    async def test_send_message_to_teams(self):
        def create_conversation():
            pass

        adapter = SimpleAdapterWithCreateConversation(
            call_create_conversation=create_conversation
        )

        turn_context = TurnContext(adapter, ACTIVITY)
        handler = TestTeamsActivityHandler()
        await handler.on_turn(turn_context)

    async def test_send_message_to_teams_channels_without_turn_context(self):
        try:
            await TeamsInfo.send_message_to_teams_channel(
                None, ACTIVITY, "channelId123"
            )
        except ValueError:
            pass
        else:
            assert False, "should have raise ValueError"

    async def test_send_message_to_teams_channels_without_teams_channel_id(self):
        def create_conversation():
            pass

        adapter = SimpleAdapterWithCreateConversation(
            call_create_conversation=create_conversation
        )

        turn_context = TurnContext(adapter, ACTIVITY)

        try:
            await TeamsInfo.send_message_to_teams_channel(turn_context, ACTIVITY, "")
        except ValueError:
            pass
        else:
            assert False, "should have raise ValueError"

    async def test_send_message_to_teams_channel_works(self):
        adapter = SimpleAdapterWithCreateConversation()

        turn_context = TurnContext(adapter, ACTIVITY)
        result = await TeamsInfo.send_message_to_teams_channel(
            turn_context, ACTIVITY, "teamId123"
        )
        assert result[0].activity_id == "new_conversation_id"
        assert result[1] == "reference123"

    async def test_get_team_details_works_without_team_id(self):
        adapter = SimpleAdapterWithCreateConversation()
        ACTIVITY.channel_data = {}
        turn_context = TurnContext(adapter, ACTIVITY)
        result = TeamsInfo.get_team_id(turn_context)

        assert result == ""

    async def test_get_team_details_works_with_team_id(self):
        adapter = SimpleAdapterWithCreateConversation()
        team_id = "teamId123"
        ACTIVITY.channel_data = {"team": {"id": team_id}}
        turn_context = TurnContext(adapter, ACTIVITY)
        result = TeamsInfo.get_team_id(turn_context)

        assert result == team_id

    async def test_get_team_details_without_team_id(self):
        def create_conversation():
            pass

        adapter = SimpleAdapterWithCreateConversation(
            call_create_conversation=create_conversation
        )

        turn_context = TurnContext(adapter, ACTIVITY)

        try:
            await TeamsInfo.get_team_details(turn_context)
        except TypeError:
            pass
        else:
            assert False, "should have raise TypeError"

    async def test_get_team_channels_without_team_id(self):
        def create_conversation():
            pass

        adapter = SimpleAdapterWithCreateConversation(
            call_create_conversation=create_conversation
        )

        turn_context = TurnContext(adapter, ACTIVITY)

        try:
            await TeamsInfo.get_team_channels(turn_context)
        except TypeError:
            pass
        else:
            assert False, "should have raise TypeError"

    async def test_get_paged_team_members_without_team_id(self):
        def create_conversation():
            pass

        adapter = SimpleAdapterWithCreateConversation(
            call_create_conversation=create_conversation
        )

        turn_context = TurnContext(adapter, ACTIVITY)

        try:
            await TeamsInfo.get_paged_team_members(turn_context)
        except TypeError:
            pass
        else:
            assert False, "should have raise TypeError"

    async def test_get_team_members_without_team_id(self):
        def create_conversation():
            pass

        adapter = SimpleAdapterWithCreateConversation(
            call_create_conversation=create_conversation
        )

        turn_context = TurnContext(adapter, ACTIVITY)

        try:
            await TeamsInfo.get_team_member(turn_context)
        except TypeError:
            pass
        else:
            assert False, "should have raise TypeError"

    async def test_get_team_members_without_member_id(self):
        def create_conversation():
            pass

        adapter = SimpleAdapterWithCreateConversation(
            call_create_conversation=create_conversation
        )

        turn_context = TurnContext(adapter, ACTIVITY)

        try:
            await TeamsInfo.get_team_member(turn_context, "teamId123")
        except TypeError:
            pass
        else:
            assert False, "should have raise TypeError"

    async def test_get_participant(self):
        adapter = SimpleAdapterWithCreateConversation()

        activity = Activity(
            type="message",
            text="Test-get_participant",
            channel_id=Channels.ms_teams,
            from_property=ChannelAccount(aad_object_id="participantId-1"),
            channel_data={
                "meeting": {"id": "meetingId-1"},
                "tenant": {"id": "tenantId-1"},
            },
            service_url="https://test.coffee",
        )

        turn_context = TurnContext(adapter, activity)
        handler = TeamsActivityHandler()
        await handler.on_turn(turn_context)

    async def test_get_meeting_info(self):
        adapter = SimpleAdapterWithCreateConversation()

        activity = Activity(
            type="message",
            text="Test-get_meeting_info",
            channel_id=Channels.ms_teams,
            from_property=ChannelAccount(aad_object_id="participantId-1"),
            channel_data={"meeting": {"id": "meetingId-1"}},
            service_url="https://test.coffee",
        )

        turn_context = TurnContext(adapter, activity)
        handler = TeamsActivityHandler()
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
