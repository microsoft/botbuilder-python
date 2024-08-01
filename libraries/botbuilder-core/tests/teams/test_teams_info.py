# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from http.server import BaseHTTPRequestHandler
import aiounittest
from botframework.connector import Channels

import json
from botbuilder.schema._models_py3 import ErrorResponse
from botbuilder.schema.teams._models_py3 import (
    TaskModuleContinueResponse,
    TaskModuleTaskInfo,
)
from botbuilder.schema.teams.meeting_stage_surface import MeetingStageSurface
from botbuilder.schema.teams.targeted_meeting_notification_value import (
    TargetedMeetingNotificationValue,
)
from simple_adapter_with_create_conversation import SimpleAdapterWithCreateConversation
from botbuilder.schema.teams.on_behalf_of import OnBehalfOf
from botbuilder.schema.teams.meeting_notification_channel_data import (
    MeetingNotificationChannelData,
)
from botbuilder.schema.teams.targeted_meeting_notification import (
    TargetedMeetingNotification,
)

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

    @staticmethod
    def get_targeted_meeting_notification(from_user) -> TargetedMeetingNotification:
        recipients = [from_user.id]

        if from_user.name == "207":
            recipients.append("failingid")

        surface = MeetingStageSurface[TaskModuleContinueResponse]()
        surface.content = TaskModuleContinueResponse(
            value=TaskModuleTaskInfo(title="title here", height=3, width=2)
        )
        surface.content_type = "Task"

        value = TargetedMeetingNotificationValue(
            recipients=recipients, surfaces=[surface]
        )

        obo = OnBehalfOf(display_name=from_user.name, mri=from_user.id)
        channel_data = MeetingNotificationChannelData(on_behalf_of_list=[obo])

        return TargetedMeetingNotification(
            value=value,
            channel_data=channel_data
        )

    @staticmethod
    async def call_send_meeting_notification_async(turn_context: TurnContext):
        from_user = turn_context.activity.from_property

        try:
            failed_participants = await TeamsInfo.send_meeting_notification_async(
                turn_context,
                TestTeamsActivityHandler.get_targeted_meeting_notification(from_user),
                "meeting-id",
            )

            if from_user.name == "207":
                assert (
                    "failingid"
                    == failed_participants.recipients_failure_info[0].recipient_mri
                )
            elif from_user.name == "202":
                assert failed_participants is None
            else:
                raise ValueError(
                    f"Expected HttpOperationException with response status code {from_user.name}"
                )

        except Exception as ex:
            assert from_user.name == str(ex.response.status_code)
            error_response = ErrorResponse.from_json(ex.response.content)

            if from_user.name == "400":
                assert "BadSyntax" == error_response.error.code
            elif from_user.name == "403":
                assert "BotNotInConversationRoster" == error_response.error.code
            else:
                raise ValueError(
                    f"Expected HttpOperationException with response status code {from_user.name}"
                )


class RosterHttpMessageHandler(BaseHTTPRequestHandler):
    async def send_async(self):
        # Set response headers
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # Route handling based on path
        path_handlers = {
            "team-id": self.handle_team_id,
            "v3/conversations": self.handle_v3_conversations,
            "team-id/conversations": self.handle_team_id_conversations,
            "team-id/members": self.handle_team_id_members,
            "conversation-id/members": self.handle_conversation_id_members,
            "team-id/members/id-1": self.handle_member_id,
            "conversation-id/members/id-1": self.handle_member_id,
            "v1/meetings/meetingId-1/participants/participantId-1?tenantId=tenantId-1": self.handle_meeting_participant,
            "v1/meetings/meeting-id": self.handle_meeting_id,
            "v1/meetings/meeting-id/notification": self.handle_meeting_notification,
        }

        path = self.path
        handler = next(
            (handler for key, handler in path_handlers.items() if path.endswith(key)),
            None,
        )
        if handler:
            response = await handler()
            self.wfile.write(response.encode("utf-8"))
        else:
            self.send_response(404)
            self.wfile.write(b"Not Found")

    async def handle_team_id(self):
        content = {
            "id": "team-id",
            "name": "team-name",
            "aadGroupId": "team-aadgroupid",
        }
        return json.dumps(content)

    async def handle_v3_conversations(self):
        content = {
            "id": "id123",
            "serviceUrl": "https://serviceUrl/",
            "activityId": "activityId123",
        }
        return json.dumps(content)

    async def handle_team_id_conversations(self):
        content = {
            "conversations": [
                {"id": "channel-id-1"},
                {"id": "channel-id-2", "name": "channel-name-2"},
                {"id": "channel-id-3", "name": "channel-name-3"},
            ]
        }
        return json.dumps(content)

    async def handle_team_id_members(self):
        content = [
            {
                "id": "id-1",
                "objectId": "objectId-1",
                "name": "name-1",
                "givenName": "givenName-1",
                "surname": "surname-1",
                "email": "email-1",
                "userPrincipalName": "userPrincipalName-1",
                "tenantId": "tenantId-1",
            },
            {
                "id": "id-2",
                "objectId": "objectId-2",
                "name": "name-2",
                "givenName": "givenName-2",
                "surname": "surname-2",
                "email": "email-2",
                "userPrincipalName": "userPrincipalName-2",
                "tenantId": "tenantId-2",
            },
        ]
        return json.dumps(content)

    async def handle_conversation_id_members(self):
        content = [
            {
                "id": "id-3",
                "objectId": "objectId-3",
                "name": "name-3",
                "givenName": "givenName-3",
                "surname": "surname-3",
                "email": "email-3",
                "userPrincipalName": "userPrincipalName-3",
                "tenantId": "tenantId-3",
            },
            {
                "id": "id-4",
                "objectId": "objectId-4",
                "name": "name-4",
                "givenName": "givenName-4",
                "surname": "surname-4",
                "email": "email-4",
                "userPrincipalName": "userPrincipalName-4",
                "tenantId": "tenantId-4",
            },
        ]
        return json.dumps(content)

    async def handle_member_id(self):
        content = {
            "id": "id-1",
            "objectId": "objectId-1",
            "name": "name-1",
            "givenName": "givenName-1",
            "surname": "surname-1",
            "email": "email-1",
            "userPrincipalName": "userPrincipalName-1",
            "tenantId": "tenantId-1",
        }
        return json.dumps(content)

    async def handle_meeting_participant(self):
        content = {
            "user": {"userPrincipalName": "userPrincipalName-1"},
            "meeting": {"role": "Organizer"},
            "conversation": {"Id": "meetigConversationId-1"},
        }
        return json.dumps(content)

    async def handle_meeting_id(self):
        content = {
            "details": {"id": "meeting-id"},
            "organizer": {"id": "organizer-id"},
            "conversation": {"id": "meetingConversationId-1"},
        }
        return json.dumps(content)

    async def handle_meeting_notification(self):
        content_length = int(self.headers["Content-Length"])
        response_body = self.rfile.read(content_length).decode("utf-8")
        notification = json.loads(response_body)
        obo = notification["ChannelData"]["OnBehalfOfList"][0]

        # hack displayname as expected status code, for testing
        display_name = obo["DisplayName"]
        if display_name == "207":
            recipient_failure_info = {
                "RecipientMri": next(
                    r
                    for r in notification["Value"]["Recipients"]
                    if r.lower() != obo["Mri"].lower()
                )
            }
            infos = {"RecipientsFailureInfo": [recipient_failure_info]}
            response = json.dumps(infos)
            status_code = 207
        elif display_name == "403":
            response = json.dumps({"error": {"code": "BotNotInConversationRoster"}})
            status_code = 403
        elif display_name == "400":
            response = json.dumps({"error": {"code": "BadSyntax"}})
            status_code = 400
        else:
            response = ""
            status_code = 202

        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        return response
