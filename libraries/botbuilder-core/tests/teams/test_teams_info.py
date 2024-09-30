# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import aiounittest
from botbuilder.schema.teams._models_py3 import (
    ContentType,
    MeetingNotificationChannelData,
    MeetingStageSurface,
    MeetingTabIconSurface,
    OnBehalfOf,
    TargetedMeetingNotification,
    TargetedMeetingNotificationValue,
    TaskModuleContinueResponse,
    TaskModuleTaskInfo,
)
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

    async def test_send_meeting_notificationt(self):
        test_cases = [
            ("202", "accepted"),
            (
                "207",
                "if the notifications are sent only to parital number of recipients\
                      because the validation on some recipients' ids failed or some\
                          recipients were not found in the roster. In this case, \
                            SMBA will return the user MRIs of those failed recipients\
                                  in a format that was given to a bot (ex: if a bot sent \
                                    encrypted user MRIs, return encrypted one).",
            ),
            (
                "400",
                "when Meeting Notification request payload validation fails. For instance,\
                      Recipients: # of recipients is greater than what the API allows ||\
                        all of recipients' user ids were invalid, Surface: Surface list\
                              is empty or null, Surface type is invalid, Duplicative \
                                surface type exists in one payload",
            ),
            (
                "403",
                "if the bot is not allowed to send the notification. In this case,\
                      the payload should contain more detail error message. \
                        There can be many reasons: bot disabled by tenant admin,\
                              blocked during live site mitigation, the bot does not\
                                  have a correct RSC permission for a specific surface type, etc",
            ),
        ]
        for status_code, expected_message in test_cases:
            adapter = SimpleAdapterWithCreateConversation()

            activity = Activity(
                type="targetedMeetingNotification",
                text="Test-send_meeting_notificationt",
                channel_id=Channels.ms_teams,
                from_property=ChannelAccount(
                    aad_object_id="participantId-1", name=status_code
                ),
                service_url="https://test.coffee",
                conversation=ConversationAccount(id="conversation-id"),
            )

            turn_context = TurnContext(adapter, activity)
            handler = TeamsActivityHandler()
            await handler.on_turn(turn_context)


class TestTeamsActivityHandler(TeamsActivityHandler):
    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        if turn_context.activity.text == "test_send_message_to_teams_channel":
            await self.call_send_message_to_teams(turn_context)
        elif turn_context.activity.text == "test_send_meeting_notification":
            await self.call_send_meeting_notification(turn_context)

    async def call_send_message_to_teams(self, turn_context: TurnContext):
        msg = MessageFactory.text("call_send_message_to_teams")
        channel_id = "teams_channel_123"
        reference = await TeamsInfo.send_message_to_teams_channel(
            turn_context, msg, channel_id
        )

        assert reference[0].activity_id == "new_conversation_id"
        assert reference[1] == "reference123"

    async def call_send_meeting_notification(self, turn_context: TurnContext):
        from_property = turn_context.activity.from_property
        try:
            # Send the meeting notification asynchronously
            failed_participants = await TeamsInfo.send_meeting_notification(
                turn_context,
                self.get_targeted_meeting_notification(from_property),
                "meeting-id",
            )

            # Handle based on the 'from_property.name'
            if from_property.name == "207":
                self.assertEqual(
                    "failingid",
                    failed_participants.recipients_failure_info[0].recipient_mri,
                )
            elif from_property.name == "202":
                assert failed_participants is None
            else:
                raise TypeError(
                    f"Expected HttpOperationException with response status code {from_property.name}."
                )

        except ValueError as ex:
            # Assert that the response status code matches the from_property.name
            assert from_property.name == str(int(ex.response.status_code))

            # Deserialize the error response content to an ErrorResponse object
            error_response = json.loads(ex.response.content)

            # Handle based on error codes
            if from_property.name == "400":
                assert error_response["error"]["code"] == "BadSyntax"
            elif from_property.name == "403":
                assert error_response["error"]["code"] == "BotNotInConversationRoster"
            else:
                raise TypeError(
                    f"Expected HttpOperationException with response status code {from_property.name}."
                )

    def get_targeted_meeting_notification(self, from_account: ChannelAccount):
        recipients = [from_account.id]

        if from_account.name == "207":
            recipients.append("failingid")

        meeting_stage_surface = MeetingStageSurface(
            content=TaskModuleContinueResponse(
                value=TaskModuleTaskInfo(title="title here", height=3, width=2)
            ),
            content_type=ContentType.Task,
        )

        meeting_tab_icon_surface = MeetingTabIconSurface(
            tab_entity_id="test tab entity id"
        )

        value = TargetedMeetingNotificationValue(
            recipients=recipients,
            surfaces=[meeting_stage_surface, meeting_tab_icon_surface],
        )

        obo = OnBehalfOf(display_name=from_account.name, mri=from_account.id)

        channel_data = MeetingNotificationChannelData(on_behalf_of_list=[obo])

        return TargetedMeetingNotification(value=value, channel_data=channel_data)
