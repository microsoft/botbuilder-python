# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import uuid4

from botbuilder.core import Storage
from botbuilder.schema import ConversationReference

from .conversation_id_factory import ConversationIdFactoryBase
from .skill_conversation_id_factory_options import SkillConversationIdFactoryOptions
from .skill_conversation_reference import SkillConversationReference


class SkillConversationIdFactory(ConversationIdFactoryBase):
    def __init__(self, storage: Storage):
        if not storage:
            raise TypeError("storage can't be None")

        self._storage = storage

    async def create_skill_conversation_id(
        self, options: SkillConversationIdFactoryOptions,
    ) -> str:
        if not options or not isinstance(options, SkillConversationIdFactoryOptions):
            raise TypeError(
                "This id factory requires a SkillConversationIdFactoryOptions instance"
            )

        # Create the storage key based on the SkillConversationIdFactoryOptions.
        conversation_reference = options.activity.get_conversation_reference()

        skill_conversation_id = uuid4()

        # Create the SkillConversationReference instance.
        skill_conversation_reference = SkillConversationReference(
            conversation_reference=conversation_reference,
            oauth_scope=options.from_bot_oauth_scope,
        )

        # Store the SkillConversationReference using the skillConversationId as a key.
        skill_conversation_info = {skill_conversation_id: skill_conversation_reference}

        await self._storage.write(skill_conversation_info)

        # Return the generated skillConversationId (that will be also used as the conversation ID to call the skill).
        return skill_conversation_id

    async def get_conversation_reference(
        self, skill_conversation_id: str
    ) -> ConversationReference:
        if not skill_conversation_id:
            raise TypeError("skill_conversation_id can't be None")

        skill_conversation_info = await self._storage.read([skill_conversation_id])

        return skill_conversation_info.get(skill_conversation_id)

    async def delete_conversation_reference(self, skill_conversation_id: str):
        await self._storage.delete([skill_conversation_id])
