# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# pylint: disable=no-member

import json
from typing import Dict, List, Tuple
from logging import Logger

import aiohttp
from botbuilder.core import InvokeResponse
from botbuilder.core.skills import BotFrameworkClient
from botbuilder.schema import (
    Activity,
    ExpectedReplies,
    ConversationReference,
    ConversationAccount,
    ChannelAccount,
    RoleTypes,
)
from botframework.connector.auth import (
    ChannelProvider,
    CredentialProvider,
    MicrosoftAppCredentials,
    AppCredentials,
    MicrosoftGovernmentAppCredentials,
)


class BotFrameworkHttpClient(BotFrameworkClient):

    """
    A skill host adapter that implements the API to forward activity to a skill and
    implements routing ChannelAPI calls from the skill up through the bot/adapter.
    """

    INVOKE_ACTIVITY_NAME = "SkillEvents.ChannelApiInvoke"
    _BOT_IDENTITY_KEY = "BotIdentity"
    _APP_CREDENTIALS_CACHE: Dict[str, MicrosoftAppCredentials] = {}

    def __init__(
        self,
        credential_provider: CredentialProvider,
        channel_provider: ChannelProvider = None,
        logger: Logger = None,
    ):
        if not credential_provider:
            raise TypeError("credential_provider can't be None")

        self._credential_provider = credential_provider
        self._channel_provider = channel_provider
        self._logger = logger
        self._session = aiohttp.ClientSession()

    async def post_activity(
        self,
        from_bot_id: str,
        to_bot_id: str,
        to_url: str,
        service_url: str,
        conversation_id: str,
        activity: Activity,
    ) -> InvokeResponse:
        app_credentials = await self._get_app_credentials(from_bot_id, to_bot_id)

        if not app_credentials:
            raise KeyError("Unable to get appCredentials to connect to the skill")

        # Get token for the skill call
        token = (
            app_credentials.get_access_token()
            if app_credentials.microsoft_app_id
            else None
        )

        # Capture current activity settings before changing them.
        original_conversation_id = activity.conversation.id
        original_service_url = activity.service_url
        original_relates_to = activity.relates_to
        original_recipient = activity.recipient

        try:
            activity.relates_to = ConversationReference(
                service_url=activity.service_url,
                activity_id=activity.id,
                channel_id=activity.channel_id,
                conversation=ConversationAccount(
                    id=activity.conversation.id,
                    name=activity.conversation.name,
                    conversation_type=activity.conversation.conversation_type,
                    aad_object_id=activity.conversation.aad_object_id,
                    is_group=activity.conversation.is_group,
                    role=activity.conversation.role,
                    tenant_id=activity.conversation.tenant_id,
                    properties=activity.conversation.properties,
                ),
                bot=None,
            )
            activity.conversation.id = conversation_id
            activity.service_url = service_url
            if not activity.recipient:
                activity.recipient = ChannelAccount(role=RoleTypes.skill)
            else:
                activity.recipient.role = RoleTypes.skill

            status, content = await self._post_content(to_url, token, activity)

            return InvokeResponse(status=status, body=content)

        finally:
            # Restore activity properties.
            activity.conversation.id = original_conversation_id
            activity.service_url = original_service_url
            activity.relates_to = original_relates_to
            activity.recipient = original_recipient

    async def _post_content(
        self, to_url: str, token: str, activity: Activity
    ) -> Tuple[int, object]:
        headers_dict = {
            "Content-type": "application/json; charset=utf-8",
        }
        if token:
            headers_dict.update(
                {
                    "Authorization": f"Bearer {token}",
                }
            )

        json_content = json.dumps(activity.serialize())
        resp = await self._session.post(
            to_url,
            data=json_content.encode("utf-8"),
            headers=headers_dict,
        )
        resp.raise_for_status()
        data = (await resp.read()).decode()
        return resp.status, json.loads(data) if data else None

    async def post_buffered_activity(
        self,
        from_bot_id: str,
        to_bot_id: str,
        to_url: str,
        service_url: str,
        conversation_id: str,
        activity: Activity,
    ) -> List[Activity]:
        """
        Helper method to return a list of activities when an Activity is being
        sent with DeliveryMode == expectReplies.
        """
        response = await self.post_activity(
            from_bot_id, to_bot_id, to_url, service_url, conversation_id, activity
        )
        if not response or (response.status / 100) != 2:
            return []
        return ExpectedReplies().deserialize(response.body).activities

    async def _get_app_credentials(
        self, app_id: str, oauth_scope: str
    ) -> AppCredentials:
        if not app_id:
            return MicrosoftAppCredentials.empty()

        # in the cache?
        cache_key = f"{app_id}{oauth_scope}"
        app_credentials = BotFrameworkHttpClient._APP_CREDENTIALS_CACHE.get(cache_key)
        if app_credentials:
            return app_credentials

        # create a new AppCredentials
        app_password = await self._credential_provider.get_app_password(app_id)

        app_credentials = (
            MicrosoftGovernmentAppCredentials(app_id, app_password, scope=oauth_scope)
            if self._channel_provider and self._channel_provider.is_government()
            else MicrosoftAppCredentials(app_id, app_password, oauth_scope=oauth_scope)
        )

        # put it in the cache
        BotFrameworkHttpClient._APP_CREDENTIALS_CACHE[cache_key] = app_credentials

        return app_credentials
