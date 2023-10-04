# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger

from botbuilder.core import InvokeResponse
from botbuilder.integration.aiohttp import BotFrameworkHttpClient
from botbuilder.core.skills import (
    ConversationIdFactoryBase,
    SkillConversationIdFactoryOptions,
    BotFrameworkSkill,
)
from botbuilder.schema import Activity
from botframework.connector.auth import (
    AuthenticationConstants,
    ChannelProvider,
    GovernmentConstants,
    SimpleCredentialProvider,
)


class SkillHttpClient(BotFrameworkHttpClient):
    def __init__(
        self,
        credential_provider: SimpleCredentialProvider,
        skill_conversation_id_factory: ConversationIdFactoryBase,
        channel_provider: ChannelProvider = None,
        logger: Logger = None,
    ):
        if not skill_conversation_id_factory:
            raise TypeError(
                "SkillHttpClient(): skill_conversation_id_factory can't be None"
            )

        super().__init__(credential_provider)

        self._skill_conversation_id_factory = skill_conversation_id_factory
        self._channel_provider = channel_provider

    async def post_activity_to_skill(
        self,
        from_bot_id: str,
        to_skill: BotFrameworkSkill,
        service_url: str,
        activity: Activity,
        originating_audience: str = None,
    ) -> InvokeResponse:
        if originating_audience is None:
            originating_audience = (
                GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
                if self._channel_provider is not None
                and self._channel_provider.is_government()
                else AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
            )

        options = SkillConversationIdFactoryOptions(
            from_bot_oauth_scope=originating_audience,
            from_bot_id=from_bot_id,
            activity=activity,
            bot_framework_skill=to_skill,
        )

        skill_conversation_id = (
            await self._skill_conversation_id_factory.create_skill_conversation_id(
                options
            )
        )

        return await super().post_activity(
            from_bot_id,
            to_skill.app_id,
            to_skill.skill_endpoint,
            service_url,
            skill_conversation_id,
            activity,
        )
