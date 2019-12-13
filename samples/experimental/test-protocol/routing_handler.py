# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.core import ChannelServiceHandler
from botbuilder.schema import (
    Activity,
    ChannelAccount,
    ConversationParameters,
    ConversationResourceResponse,
    ConversationsResult,
    PagedMembersResult,
    ResourceResponse
)
from botframework.connector.aio import ConnectorClient
from botframework.connector.auth import (
    AuthenticationConfiguration,
    ChannelProvider,
    ClaimsIdentity,
    CredentialProvider,
    MicrosoftAppCredentials
)

from routing_id_factory import RoutingIdFactory


class RoutingHandler(ChannelServiceHandler):
    def __init__(
        self,
        conversation_id_factory: RoutingIdFactory,
        credential_provider: CredentialProvider,
        auth_configuration: AuthenticationConfiguration,
        channel_provider: ChannelProvider = None
    ):
        super().__init__(credential_provider, auth_configuration, channel_provider)
        self._factory = conversation_id_factory
        self._credentials = MicrosoftAppCredentials(None, None)

    async def on_reply_to_activity(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity_id: str,
        activity: Activity,
    ) -> ResourceResponse:
        back_conversation_id, back_service_url = self._factory.get_conversation_info(conversation_id)
        connector_client = self._get_connector_client(back_service_url)
        activity.conversation.id = back_conversation_id
        activity.service_url = back_service_url

        return await connector_client.conversations.send_to_conversation(back_conversation_id, activity)

    async def on_send_to_conversation(
        self, claims_identity: ClaimsIdentity, conversation_id: str, activity: Activity,
    ) -> ResourceResponse:
        back_conversation_id, back_service_url = self._factory.get_conversation_info(conversation_id)
        connector_client = self._get_connector_client(back_service_url)
        activity.conversation.id = back_conversation_id
        activity.service_url = back_service_url

        return await connector_client.conversations.send_to_conversation(back_conversation_id, activity)

    async def on_update_activity(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity_id: str,
        activity: Activity,
    ) -> ResourceResponse:
        back_conversation_id, back_service_url = self._factory.get_conversation_info(conversation_id)
        connector_client = self._get_connector_client(back_service_url)
        activity.conversation.id = back_conversation_id
        activity.service_url = back_service_url

        return await connector_client.conversations.update_activity(back_conversation_id, activity.id, activity)

    async def on_delete_activity(
        self, claims_identity: ClaimsIdentity, conversation_id: str, activity_id: str,
    ):
        back_conversation_id, back_service_url = self._factory.get_conversation_info(conversation_id)
        connector_client = self._get_connector_client(back_service_url)

        return await connector_client.conversations.delete_activity(back_conversation_id, activity_id)

    async def on_create_conversation(
        self, claims_identity: ClaimsIdentity, parameters: ConversationParameters,
    ) -> ConversationResourceResponse:
        # This call will be used in Teams scenarios.

        # Scenario #1 - creating a thread with an activity in a Channel in a Team
        # In order to know the serviceUrl in the case of Teams we would need to look it up based upon the
        # TeamsChannelData.
        # The inbound activity will contain the TeamsChannelData and so will the ConversationParameters.

        # Scenario #2 - starting a one on one conversation with a particular user
        # - needs further analysis -

        back_service_url = "http://tempuri"
        connector_client = self._get_connector_client(back_service_url)

        return await connector_client.conversations.create_conversation(parameters)

    async def on_delete_conversation_member(
        self, claims_identity: ClaimsIdentity, conversation_id: str, member_id: str,
    ):
        return await super().on_delete_conversation_member(claims_identity, conversation_id, member_id)

    async def on_get_activity_members(
        self, claims_identity: ClaimsIdentity, conversation_id: str, activity_id: str,
    ) -> List[ChannelAccount]:
        return await super().on_get_activity_members(claims_identity, conversation_id, activity_id)

    async def on_get_conversation_members(
        self, claims_identity: ClaimsIdentity, conversation_id: str,
    ) -> List[ChannelAccount]:
        return await super().on_get_conversation_members(claims_identity, conversation_id)

    async def on_get_conversations(
        self, claims_identity: ClaimsIdentity, continuation_token: str = "",
    ) -> ConversationsResult:
        return await super().on_get_conversations(claims_identity, continuation_token)

    async def on_get_conversation_paged_members(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        page_size: int = None,
        continuation_token: str = "",
    ) -> PagedMembersResult:
        return await super().on_get_conversation_paged_members(claims_identity, conversation_id, continuation_token)

    def _get_connector_client(self, service_url: str):
        return ConnectorClient(self._credentials, service_url)
