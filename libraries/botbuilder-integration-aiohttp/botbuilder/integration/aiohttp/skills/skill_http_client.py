from logging import Logger

from botbuilder.schema import Activity
from botframework.connector.auth import (
    ChannelProvider,
    CredentialProvider,
)
from botbuilder.core import InvokeResponse, TurnContext
from botbuilder.core.skills import BotFrameworkSkill, SkillConversationIdFactory
from botbuilder.integration.aiohttp import BotFrameworkHttpClient


class SkillHttpClient(BotFrameworkHttpClient):
    def __init__(
        self,
        credential_provider: CredentialProvider,
        conversation_id_factory: SkillConversationIdFactory,
        channel_provider: ChannelProvider = None,
        logger: Logger = None,
    ):
        super().__init__(credential_provider, channel_provider, logger)
        self._conversation_id_factory = conversation_id_factory

    async def post_activity(
        self,
        from_bot_id: str,
        to_skill: BotFrameworkSkill,
        callback_url: str,
        activity: Activity,
    ) -> InvokeResponse:
        skill_conversation_id = await self._conversation_id_factory.create_skill_conversation_id(
            TurnContext.get_conversation_reference(activity)
        )

        return await super().post_activity(
            from_bot_id,
            to_skill.app_id,
            to_skill.skill_endpoint,
            callback_url,
            skill_conversation_id,
            activity,
        )
