# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import hashlib
from typing import Dict, Tuple

from botbuilder.core import Storage
from botbuilder.schema import ConversationReference

from .conversation_id_factory import ConversationIdFactoryBase


class SkillConversationIdFactory(ConversationIdFactoryBase):
    def __init__(self, storage: Storage):
        if not storage:
            raise TypeError("storage can't be None")

        self._storage = storage
        self._forward_x_ref: Dict[str, str] = {}
        self._backward_x_ref: Dict[str, Tuple[str, str]] = {}

    async def create_skill_conversation_id(
        self, conversation_reference: ConversationReference
    ) -> str:
        if not conversation_reference:
            raise TypeError("conversation_reference can't be None")

        if not conversation_reference.conversation.id:
            raise TypeError("conversation id in conversation reference can't be None")

        if not conversation_reference.channel_id:
            raise TypeError("channel id in conversation reference can't be None")

        storage_key = hashlib.md5(
            f"{conversation_reference.conversation.id}{conversation_reference.channel_id}".encode()
        ).hexdigest()

        skill_conversation_info = {storage_key: conversation_reference}

        await self._storage.write(skill_conversation_info)

        return storage_key

    async def get_conversation_reference(
        self, skill_conversation_id: str
    ) -> ConversationReference:
        if not skill_conversation_id:
            raise TypeError("skill_conversation_id can't be None")

        skill_conversation_info = await self._storage.read([skill_conversation_id])

        return skill_conversation_info.get(skill_conversation_id)

    async def delete_conversation_reference(self, skill_conversation_id: str):
        await self._storage.delete([skill_conversation_id])
