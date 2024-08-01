import aiohttp
from typing import Optional
from botbuilder.schema.teams._models_py3 import (
    ConversationList,
    MeetingInfo,
    TeamDetails,
    TeamsMeetingParticipant,
)
from botbuilder.schema.teams.meeting_notification_base import MeetingNotificationBase
from botbuilder.schema.teams.meeting_notification_response import (
    MeetingNotificationResponse,
)
from botframework.connector.teams.operations.teams_operations import TeamsOperations


class TeamsOperationsExtensions:
    @staticmethod
    async def fetch_channel_list_async(
        operations: TeamsOperations, team_id: str
    ) -> ConversationList:
        result = await operations.get_teams_channels(team_id)
        return result.body

    @staticmethod
    async def fetch_team_details_async(
        operations: TeamsOperations, team_id: str
    ) -> TeamDetails:
        result = await operations.get_team_details(team_id)
        return result.body

    @staticmethod
    async def fetch_meeting_info_async(
        operations: TeamsOperations, meeting_id: str
    ) -> MeetingInfo:
        if not isinstance(operations, TeamsOperations):
            raise ValueError(
                "TeamsOperations with GetMeetingInfoWithHttpMessages is required for FetchMeetingInfo."
            )
        result = await operations.fetch_meeting(meeting_id)
        return result.body

    @staticmethod
    async def fetch_participant_async(
        operations: TeamsOperations,
        meeting_id: str,
        participant_id: str,
        tenant_id: str,
    ) -> TeamsMeetingParticipant:
        if not isinstance(operations, TeamsOperations):
            raise ValueError(
                "TeamsOperations with GetParticipantWithHttpMessages is required for FetchParticipant."
            )
        result = await operations.fetch_participant(
            meeting_id, participant_id, tenant_id
        )
        return result.body

    @staticmethod
    async def send_meeting_notification_async(
        operations: TeamsOperations,
        meeting_id: str,
        notification: MeetingNotificationBase,
    ) -> MeetingNotificationResponse:
        if not isinstance(operations, TeamsOperations):
            raise ValueError(
                "TeamsOperations with SendMeetingNotificationWithHttpMessages is required for SendMeetingNotification."
            )
        result = await operations.send_meeting_notification_message_async(
            meeting_id, notification
        )
        return result.body
