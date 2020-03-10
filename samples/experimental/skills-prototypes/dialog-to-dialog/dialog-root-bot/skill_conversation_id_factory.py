# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import Union

from botbuilder.core import Storage, TurnContext
from botbuilder.core.skills import (
    ConversationIdFactoryBase,
    SkillConversationIdFactoryOptions,
    SkillConversationReference,
)
from botbuilder.schema import ConversationReference


class SkillConversationIdFactory(ConversationIdFactoryBase):
    def __init__(self, storage: Storage):
        if not storage:
            raise TypeError("storage can't be None")

        self._storage = storage

    async def create_skill_conversation_id(
        self,
        options_or_conversation_reference: Union[
            SkillConversationIdFactoryOptions, ConversationReference
        ],
    ) -> str:
        if not options_or_conversation_reference:
            raise TypeError("Need options or conversation reference")

        if not isinstance(
            options_or_conversation_reference, SkillConversationIdFactoryOptions
        ):
            raise TypeError(
                "This SkillConversationIdFactory can only handle SkillConversationIdFactoryOptions"
            )

        options = options_or_conversation_reference
        conversation_reference = TurnContext.get_conversation_reference(
            options.activity
        )
        storage_key = f"{conversation_reference.conversation.id}" \
                      f"-{options.bot_framework_skill.id}" \
                      f"-{conversation_reference.channel_id}" \
                      f"-skillconvo"

        skill_conversation_reference = SkillConversationReference(
            conversation_reference=conversation_reference,
            oauth_scope=options.from_bot_oauth_scope,
        )

        skill_conversation_info = {storage_key: skill_conversation_reference}

        await self._storage.write(skill_conversation_info)

        return storage_key

    async def get_conversation_reference(
        self, skill_conversation_id: str
    ) -> Union[SkillConversationReference, ConversationReference]:
        if not skill_conversation_id:
            raise TypeError("skill_conversation_id can't be None")

        skill_conversation_info = await self._storage.read([skill_conversation_id])

        return skill_conversation_info.get(skill_conversation_id)

    async def delete_conversation_reference(self, skill_conversation_id: str):
        await self._storage.delete([skill_conversation_id])
