from botbuilder.core import BotFrameworkHttpClient, InvokeResponse, TurnContext
from botbuilder.core.skills import BotFrameworkSkill, ConversationIdFactoryBase
from botbuilder.schema import Activity


class SkillHttpClient(BotFrameworkHttpClient):
    def __init__(self, credential_provider, conversation_id_factory, channel_provider=None):
        super().__init__(credential_provider, channel_provider)

        self._conversation_id_factory: ConversationIdFactoryBase = conversation_id_factory

    async def post_activity_to_skill(
        self,
        from_bot_id: str,
        to_skill: BotFrameworkSkill,
        callback_url: str,
        activity: Activity,
    ) -> InvokeResponse:
        skill_conversation_id = await self._conversation_id_factory.create_skill_conversation_id(
            TurnContext.get_conversation_reference(activity)
        )

        return await self.post_activity(
            from_bot_id,
            to_skill.app_id,
            to_skill.skill_endpoint,
            callback_url,
            skill_conversation_id,
            activity
        )
