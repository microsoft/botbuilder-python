# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import TurnContext, Storage
from botbuilder.core.skills import (
    ConversationIdFactoryBase,
    SkillConversationIdFactoryOptions,
    SkillConversationReference,
)
from botbuilder.schema import ConversationReference
from uuid import uuid4 as uuid

class SkillConversationIdFactory(ConversationIdFactoryBase):
    def __init__(self, storage: Storage):
        if not storage:
            raise TypeError("storage can't be None")

        self._storage = storage

    async def create_skill_conversation_id(
        self,
        options: SkillConversationIdFactoryOptions
    ) -> str:
        if not options:
            raise TypeError("SkillConversationIdFactory() options can't be None")

        conversation_reference = TurnContext.get_conversation_reference(options.activity)

        skill_conversation_id = str(uuid())

        skill_conversation_reference = SkillConversationReference(
            conversation_reference=ConversationReference(conversation_reference),
            oauth_scope=options.from_bot_oauth_scope
        )

        skill_conversation_info = { [skill_conversation_id]: skill_conversation_reference }

        await self._storage.write(skill_conversation_info)

        return skill_conversation_id

    async def get_conversation_reference(
        self, 
        skill_conversation_id: str
    ) -> SkillConversationReference:
        if not skill_conversation_id:
            raise TypeError("skill_conversation_id can't be None")

        skill_conversation_reference = await self._storage.read([skill_conversation_id])
        if not skill_conversation_reference:
            raise TypeError("skill_conversation_reference")

        return SkillConversationReference(skill_conversation_reference)

    async def delete_conversation_reference(
        self,
        skill_conversation_id: str
    ):
        await self._storage.delete([skill_conversation_id])
