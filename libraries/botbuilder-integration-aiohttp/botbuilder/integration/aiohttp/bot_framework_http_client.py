# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# pylint: disable=no-member

import json
from typing import Dict
from logging import Logger

import aiohttp
from botbuilder.core import InvokeResponse
from botbuilder.core.skills import BotFrameworkClient
from botbuilder.schema import (
    Activity,
    ExpectedReplies,
    ConversationReference,
    ConversationAccount,
)
from botframework.connector.auth import (
    ChannelProvider,
    CredentialProvider,
    GovernmentConstants,
    MicrosoftAppCredentials,
)


class BotFrameworkHttpClient(BotFrameworkClient):

    """
    A skill host adapter implements API to forward activity to a skill and
    implements routing ChannelAPI calls from the Skill up through the bot/adapter.
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
        # TODO: DO we need to set the activity ID? (events that are created manually don't have it).
        original_conversation_id = activity.conversation.id
        original_service_url = activity.service_url
        original_caller_id = activity.caller_id
        original_relates_to = activity.relates_to

        try:
            # TODO: The relato has to be ported to the adapter in the new integration library when
            #  resolving conflicts in merge
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
            activity.caller_id = f"urn:botframework:aadappid:{from_bot_id}"

            headers_dict = {
                "Content-type": "application/json; charset=utf-8",
            }
            if token:
                headers_dict.update(
                    {"Authorization": f"Bearer {token}",}
                )

            json_content = json.dumps(activity.serialize())
            resp = await self._session.post(
                to_url, data=json_content.encode("utf-8"), headers=headers_dict,
            )
            resp.raise_for_status()
            data = (await resp.read()).decode()
            content = json.loads(data) if data else None

            if content:
                return InvokeResponse(status=resp.status, body=content)

        finally:
            # Restore activity properties.
            activity.conversation.id = original_conversation_id
            activity.service_url = original_service_url
            activity.caller_id = original_caller_id
            activity.relates_to = original_relates_to

    async def post_buffered_activity(
        self,
        from_bot_id: str,
        to_bot_id: str,
        to_url: str,
        service_url: str,
        conversation_id: str,
        activity: Activity,
    ) -> [Activity]:
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
    ) -> MicrosoftAppCredentials:
        if not app_id:
            return MicrosoftAppCredentials(None, None)

        cache_key = f"{app_id}{oauth_scope}"
        app_credentials = BotFrameworkHttpClient._APP_CREDENTIALS_CACHE.get(cache_key)

        if app_credentials:
            return app_credentials

        app_password = await self._credential_provider.get_app_password(app_id)
        app_credentials = MicrosoftAppCredentials(
            app_id, app_password, oauth_scope=oauth_scope
        )
        if self._channel_provider and self._channel_provider.is_government():
            app_credentials.oauth_endpoint = (
                GovernmentConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL
            )
            app_credentials.oauth_scope = (
                GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
            )

        BotFrameworkHttpClient._APP_CREDENTIALS_CACHE[cache_key] = app_credentials
        return app_credentials
