# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List, Tuple

from botframework.connector import Channels
from botframework.connector.aio import ConnectorClient
from botframework.connector.teams import TeamsConnectorClient
from botbuilder.core.teams.teams_activity_extensions import (
    teams_get_meeting_info,
    teams_get_channel_data,
)
from botbuilder.core import (
    CloudAdapterBase,
    BotFrameworkAdapter,
    TurnContext,
    BotAdapter,
)
from botbuilder.schema import Activity, ConversationParameters, ConversationReference
from botbuilder.schema.teams import (
    ChannelInfo,
    MeetingInfo,
    TeamDetails,
    TeamsChannelData,
    TeamsChannelAccount,
    TeamsPagedMembersResult,
    TeamsMeetingParticipant,
)


class TeamsInfo:
    @staticmethod
    async def send_message_to_teams_channel(
        turn_context: TurnContext,
        activity: Activity,
        teams_channel_id: str,
        *,
        bot_app_id: str = None,
    ) -> Tuple[ConversationReference, str]:
        if not turn_context:
            raise ValueError("The turn_context cannot be None")
        if not turn_context.activity:
            raise ValueError("The activity inside turn context cannot be None")
        if not activity:
            raise ValueError("The activity cannot be None")
        if not teams_channel_id:
            raise ValueError("The teams_channel_id cannot be None or empty")

        if not bot_app_id:
            return await TeamsInfo._legacy_send_message_to_teams_channel(
                turn_context, activity, teams_channel_id
            )

        conversation_reference: ConversationReference = None
        new_activity_id = ""
        service_url = turn_context.activity.service_url
        conversation_parameters = ConversationParameters(
            is_group=True,
            channel_data=TeamsChannelData(channel=ChannelInfo(id=teams_channel_id)),
            activity=activity,
        )

        async def aux_callback(
            new_turn_context,
        ):
            nonlocal new_activity_id
            nonlocal conversation_reference
            new_activity_id = new_turn_context.activity.id
            conversation_reference = TurnContext.get_conversation_reference(
                new_turn_context.activity
            )

        adapter: CloudAdapterBase = turn_context.adapter
        await adapter.create_conversation(
            bot_app_id,
            aux_callback,
            conversation_parameters,
            Channels.ms_teams,
            service_url,
            None,
        )

        return (conversation_reference, new_activity_id)

    @staticmethod
    async def _legacy_send_message_to_teams_channel(
        turn_context: TurnContext, activity: Activity, teams_channel_id: str
    ) -> Tuple[ConversationReference, str]:
        old_ref = TurnContext.get_conversation_reference(turn_context.activity)
        conversation_parameters = ConversationParameters(
            is_group=True,
            channel_data={"channel": {"id": teams_channel_id}},
            activity=activity,
        )

        # if this version of the method is called the adapter probably wont be CloudAdapter
        adapter: BotFrameworkAdapter = turn_context.adapter
        result = await adapter.create_conversation(
            old_ref, TeamsInfo._create_conversation_callback, conversation_parameters
        )
        return (result[0], result[1])

    @staticmethod
    async def _create_conversation_callback(
        new_turn_context,
    ) -> Tuple[ConversationReference, str]:
        new_activity_id = new_turn_context.activity.id
        conversation_reference = TurnContext.get_conversation_reference(
            new_turn_context.activity
        )
        return (conversation_reference, new_activity_id)

    @staticmethod
    async def get_team_details(
        turn_context: TurnContext, team_id: str = ""
    ) -> TeamDetails:
        if not team_id:
            team_id = TeamsInfo.get_team_id(turn_context)

        if not team_id:
            raise TypeError(
                "TeamsInfo.get_team_details: method is only valid within the scope of MS Teams Team."
            )

        teams_connector = await TeamsInfo.get_teams_connector_client(turn_context)
        return teams_connector.teams.get_team_details(team_id)

    @staticmethod
    async def get_team_channels(
        turn_context: TurnContext, team_id: str = ""
    ) -> List[ChannelInfo]:
        if not team_id:
            team_id = TeamsInfo.get_team_id(turn_context)

        if not team_id:
            raise TypeError(
                "TeamsInfo.get_team_channels: method is only valid within the scope of MS Teams Team."
            )

        teams_connector = await TeamsInfo.get_teams_connector_client(turn_context)
        return teams_connector.teams.get_teams_channels(team_id).conversations

    @staticmethod
    async def get_team_members(
        turn_context: TurnContext, team_id: str = ""
    ) -> List[TeamsChannelAccount]:
        if not team_id:
            team_id = TeamsInfo.get_team_id(turn_context)

        if not team_id:
            raise TypeError(
                "TeamsInfo.get_team_members: method is only valid within the scope of MS Teams Team."
            )

        connector_client = await TeamsInfo._get_connector_client(turn_context)
        return await TeamsInfo._get_members(
            connector_client,
            turn_context.activity.conversation.id,
        )

    @staticmethod
    async def get_members(turn_context: TurnContext) -> List[TeamsChannelAccount]:
        team_id = TeamsInfo.get_team_id(turn_context)
        if not team_id:
            conversation_id = turn_context.activity.conversation.id
            connector_client = await TeamsInfo._get_connector_client(turn_context)
            return await TeamsInfo._get_members(connector_client, conversation_id)

        return await TeamsInfo.get_team_members(turn_context, team_id)

    @staticmethod
    async def get_paged_team_members(
        turn_context: TurnContext,
        team_id: str = "",
        continuation_token: str = None,
        page_size: int = None,
    ) -> List[TeamsPagedMembersResult]:
        if not team_id:
            team_id = TeamsInfo.get_team_id(turn_context)

        if not team_id:
            raise TypeError(
                "TeamsInfo.get_team_members: method is only valid within the scope of MS Teams Team."
            )

        connector_client = await TeamsInfo._get_connector_client(turn_context)
        return await TeamsInfo._get_paged_members(
            connector_client,
            team_id,
            continuation_token,
            page_size,
        )

    @staticmethod
    async def get_paged_members(
        turn_context: TurnContext, continuation_token: str = None, page_size: int = None
    ) -> List[TeamsPagedMembersResult]:
        team_id = TeamsInfo.get_team_id(turn_context)
        if not team_id:
            conversation_id = turn_context.activity.conversation.id
            connector_client = await TeamsInfo._get_connector_client(turn_context)
            return await TeamsInfo._get_paged_members(
                connector_client, conversation_id, continuation_token, page_size
            )

        return await TeamsInfo.get_paged_team_members(
            turn_context, team_id, continuation_token, page_size
        )

    @staticmethod
    async def get_team_member(
        turn_context: TurnContext, team_id: str = "", member_id: str = None
    ) -> TeamsChannelAccount:
        if not team_id:
            team_id = TeamsInfo.get_team_id(turn_context)

        if not team_id:
            raise TypeError(
                "TeamsInfo.get_team_member: method is only valid within the scope of MS Teams Team."
            )

        if not member_id:
            raise TypeError("TeamsInfo.get_team_member: method requires a member_id")

        connector_client = await TeamsInfo._get_connector_client(turn_context)
        return await TeamsInfo._get_member(
            connector_client, turn_context.activity.conversation.id, member_id
        )

    @staticmethod
    async def get_member(
        turn_context: TurnContext, member_id: str
    ) -> TeamsChannelAccount:
        team_id = TeamsInfo.get_team_id(turn_context)
        if not team_id:
            conversation_id = turn_context.activity.conversation.id
            connector_client = await TeamsInfo._get_connector_client(turn_context)
            return await TeamsInfo._get_member(
                connector_client, conversation_id, member_id
            )

        return await TeamsInfo.get_team_member(turn_context, team_id, member_id)

    @staticmethod
    async def get_meeting_participant(
        turn_context: TurnContext,
        meeting_id: str = None,
        participant_id: str = None,
        tenant_id: str = None,
    ) -> TeamsMeetingParticipant:
        meeting_id = (
            meeting_id
            if meeting_id
            else teams_get_meeting_info(turn_context.activity).id
        )
        if meeting_id is None:
            raise TypeError(
                "TeamsInfo._get_meeting_participant: method requires a meeting_id"
            )

        participant_id = (
            participant_id
            if participant_id
            else turn_context.activity.from_property.aad_object_id
        )
        if participant_id is None:
            raise TypeError(
                "TeamsInfo._get_meeting_participant: method requires a participant_id"
            )

        tenant_id = (
            tenant_id
            if tenant_id
            else teams_get_channel_data(turn_context.activity).tenant.id
        )
        if tenant_id is None:
            raise TypeError(
                "TeamsInfo._get_meeting_participant: method requires a tenant_id"
            )

        connector_client = await TeamsInfo.get_teams_connector_client(turn_context)
        return connector_client.teams.fetch_participant(
            meeting_id, participant_id, tenant_id
        )

    @staticmethod
    async def get_meeting_info(
        turn_context: TurnContext, meeting_id: str = None
    ) -> MeetingInfo:
        meeting_id = (
            meeting_id
            if meeting_id
            else teams_get_meeting_info(turn_context.activity).id
        )
        if meeting_id is None:
            raise TypeError(
                "TeamsInfo._get_meeting_participant: method requires a meeting_id or "
                "TurnContext that contains a meeting id"
            )

        connector_client = await TeamsInfo.get_teams_connector_client(turn_context)
        return connector_client.teams.fetch_meeting(meeting_id)

    @staticmethod
    async def get_teams_connector_client(
        turn_context: TurnContext,
    ) -> TeamsConnectorClient:
        # A normal connector client is retrieved in order to use the credentials
        # while creating a TeamsConnectorClient below
        connector_client = await TeamsInfo._get_connector_client(turn_context)

        return TeamsConnectorClient(
            connector_client.config.credentials,
            turn_context.activity.service_url,
        )

    @staticmethod
    def get_team_id(turn_context: TurnContext):
        channel_data = TeamsChannelData(**turn_context.activity.channel_data)
        if channel_data.team:
            return channel_data.team["id"]
        return ""

    @staticmethod
    async def _get_connector_client(turn_context: TurnContext) -> ConnectorClient:
        connector_client = turn_context.turn_state.get(
            BotAdapter.BOT_CONNECTOR_CLIENT_KEY
        )

        if connector_client is None:
            raise ValueError("This method requires a connector client.")

        return connector_client

    @staticmethod
    async def _get_members(
        connector_client: ConnectorClient, conversation_id: str
    ) -> List[TeamsChannelAccount]:
        if connector_client is None:
            raise TypeError("TeamsInfo._get_members.connector_client: cannot be None.")

        if not conversation_id:
            raise TypeError("TeamsInfo._get_members.conversation_id: cannot be empty.")

        teams_members = []
        members = await connector_client.conversations.get_conversation_members(
            conversation_id
        )

        for member in members:
            teams_members.append(
                TeamsChannelAccount().deserialize(
                    dict(member.serialize(), **member.additional_properties)
                )
            )

        return teams_members

    @staticmethod
    async def _get_paged_members(
        connector_client: ConnectorClient,
        conversation_id: str,
        continuation_token: str = None,
        page_size: int = None,
    ) -> List[TeamsPagedMembersResult]:
        if connector_client is None:
            raise TypeError(
                "TeamsInfo._get_paged_members.connector_client: cannot be None."
            )

        if not conversation_id:
            raise TypeError(
                "TeamsInfo._get_paged_members.conversation_id: cannot be empty."
            )

        return (
            await connector_client.conversations.get_teams_conversation_paged_members(
                conversation_id, page_size, continuation_token
            )
        )

    @staticmethod
    async def _get_member(
        connector_client: ConnectorClient, conversation_id: str, member_id: str
    ) -> TeamsChannelAccount:
        if connector_client is None:
            raise TypeError("TeamsInfo._get_member.connector_client: cannot be None.")

        if not conversation_id:
            raise TypeError("TeamsInfo._get_member.conversation_id: cannot be empty.")

        if not member_id:
            raise TypeError("TeamsInfo._get_member.member_id: cannot be empty.")

        member: TeamsChannelAccount = (
            await connector_client.conversations.get_conversation_member(
                conversation_id, member_id
            )
        )

        return TeamsChannelAccount().deserialize(
            dict(member.serialize(), **member.additional_properties)
        )
