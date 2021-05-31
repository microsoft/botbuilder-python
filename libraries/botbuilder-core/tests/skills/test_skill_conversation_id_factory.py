from botbuilder.core import (
    MemoryStorage,
)
from botbuilder.core.skills import (
    ConversationIdFactoryBase,
    SkillConversationIdFactory,
    BotFrameworkSkill,
    SkillConversationIdFactoryOptions,
)
from botbuilder.schema import (
    Activity,
    ConversationAccount,
    ConversationReference,
)
from uuid import uuid4 as uuid

class SkillConversationIdFactoryForTest(ConversationIdFactoryBase):
    SERVICE_URL = "http://testbot.com/api/messages"
    SKILL_ID = "skill"

    def __init__(self):
        self._skill_conversation_id_factory = SkillConversationIdFactory(MemoryStorage())
        self._application_id = str(uuid())
        self._bot_id = str(uuid())
    

    async def test_skill_conversation_id_factory_happy_path(
        self
    ):
        conversation_reference = ConversationReference(
            conversation=ConversationAccount(str(uuid)),
            service_url=self.SERVICE_URL
        )

        # Create skill conversation
        skill_conversation_id = await self._skill_conversation_id_factory.create_skill_conversation_id(
            options= SkillConversationIdFactoryOptions(
                activity=self._build_message_activity(conversation_reference),
                bot_framework_skill=self._build_bot_framework_skill,
                from_bot_id=self._bot_id,
                from_bot_oauth_scope=self._bot_id
            )
        )



    def _build_message_activity(
        self,
        conversation_reference: ConversationReference
    ) -> Activity:
        if not conversation_reference:
            raise TypeError(str(conversation_reference))

        activity = Activity.create_message_activity()
        activity.apply_conversation_reference(conversation_reference)

        return activity

    def _build_bot_framework_skill(
        self
    ) -> BotFrameworkSkill:
        return BotFrameworkSkill(
            app_id=self._application_id,
            id=self.SKILL_ID,
            skill_endpoint=""
        )
