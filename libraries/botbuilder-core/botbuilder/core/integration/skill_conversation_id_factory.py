# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from typing import Tuple


class SkillConversationIdFactory(ABC):
    @abstractmethod
    def create_skill_conversation_id(
        self, conversation_id: str, service_url: str
    ) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_conversation_info(self, encoded_conversation_id: str) -> Tuple[str, str]:
        raise NotImplementedError()
