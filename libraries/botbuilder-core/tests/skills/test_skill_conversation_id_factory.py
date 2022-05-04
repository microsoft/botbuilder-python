# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import uuid4 as uuid
from aiounittest import AsyncTestCase
from botbuilder.core import MemoryStorage
from botbuilder.schema import (
    Activity,
    ConversationAccount,
    ConversationReference,
)
from botbuilder.core.skills import (
    BotFrameworkSkill,
    SkillConversationIdFactory,
    SkillConversationIdFactoryOptions,
)


class SkillConversationIdFactoryForTest(AsyncTestCase):
    SERVICE_URL = "http://testbot.com/api/messages"
    SKILL_ID = "skill"

    @classmethod
    def setUpClass(cls):
        cls._skill_conversation_id_factory = SkillConversationIdFactory(MemoryStorage())
        cls._application_id = str(uuid())
        cls._bot_id = str(uuid())

    async def test_skill_conversation_id_factory_happy_path(self):
        conversation_reference = self._build_conversation_reference()

        # Create skill conversation
        skill_conversation_id = (
            await self._skill_conversation_id_factory.create_skill_conversation_id(
                options=SkillConversationIdFactoryOptions(
                    activity=self._build_message_activity(conversation_reference),
                    bot_framework_skill=self._build_bot_framework_skill(),
                    from_bot_id=self._bot_id,
                    from_bot_oauth_scope=self._bot_id,
                )
            )
        )

        assert (
            skill_conversation_id and skill_conversation_id.strip()
        ), "Expected a valid skill conversation ID to be created"

        # Retrieve skill conversation
        retrieved_conversation_reference = (
            await self._skill_conversation_id_factory.get_skill_conversation_reference(
                skill_conversation_id
            )
        )

        # Delete
        await self._skill_conversation_id_factory.delete_conversation_reference(
            skill_conversation_id
        )

        # Retrieve again
        deleted_conversation_reference = (
            await self._skill_conversation_id_factory.get_skill_conversation_reference(
                skill_conversation_id
            )
        )

        self.assertIsNotNone(retrieved_conversation_reference)
        self.assertIsNotNone(retrieved_conversation_reference.conversation_reference)
        self.assertEqual(
            conversation_reference,
            retrieved_conversation_reference.conversation_reference,
        )
        self.assertIsNone(deleted_conversation_reference)

    async def test_id_is_unique_each_time(self):
        conversation_reference = self._build_conversation_reference()

        # Create skill conversation
        first_id = (
            await self._skill_conversation_id_factory.create_skill_conversation_id(
                options=SkillConversationIdFactoryOptions(
                    activity=self._build_message_activity(conversation_reference),
                    bot_framework_skill=self._build_bot_framework_skill(),
                    from_bot_id=self._bot_id,
                    from_bot_oauth_scope=self._bot_id,
                )
            )
        )

        second_id = (
            await self._skill_conversation_id_factory.create_skill_conversation_id(
                options=SkillConversationIdFactoryOptions(
                    activity=self._build_message_activity(conversation_reference),
                    bot_framework_skill=self._build_bot_framework_skill(),
                    from_bot_id=self._bot_id,
                    from_bot_oauth_scope=self._bot_id,
                )
            )
        )

        # Ensure that we get a different conversation_id each time we call create_skill_conversation_id
        self.assertNotEqual(first_id, second_id)

    def _build_conversation_reference(self) -> ConversationReference:
        return ConversationReference(
            conversation=ConversationAccount(id=str(uuid())),
            service_url=self.SERVICE_URL,
        )

    def _build_message_activity(
        self, conversation_reference: ConversationReference
    ) -> Activity:
        if not conversation_reference:
            raise TypeError(str(conversation_reference))

        activity = Activity.create_message_activity()
        activity.apply_conversation_reference(conversation_reference)

        return activity

    def _build_bot_framework_skill(self) -> BotFrameworkSkill:
        return BotFrameworkSkill(
            app_id=self._application_id,
            id=self.SKILL_ID,
            skill_endpoint=self.SERVICE_URL,
        )
