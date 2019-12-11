# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from abc import ABC, abstractmethod
from botbuilder.schema import ConversationReference


class ConversationIdFactoryBase(ABC):
    @abstractmethod
    async def create_skill_conversation_id(
        self, conversation_reference: ConversationReference
    ) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def get_conversation_reference(
        self, skill_conversation_id: str
    ) -> ConversationReference:
        raise NotImplementedError()

    @abstractmethod
    async def delete_conversation_reference(self, skill_conversation_id: str):
        raise NotImplementedError()
