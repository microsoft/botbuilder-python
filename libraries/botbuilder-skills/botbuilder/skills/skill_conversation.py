# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import base64
import json

from typing import List


class SkillConversation:
    def __init__(
        self,
        packed_conversation_id: str = None,
        conversation_id: str = None,
        service_url: str = None,
    ):
        if packed_conversation_id:
            parts: List[str] = json.loads(
                base64.b64decode(packed_conversation_id).decode("utf-8")
            )

            self.conversation_id = parts[0]
            self.service_url = parts[1]
        else:
            self.conversation_id = conversation_id
            self.service_url = service_url

    def get_skill_conversation_id(self) -> str:
        """
        Get packed skill conversation_id
        :return: packed conversation_id
        """
        if not self.conversation_id:
            raise TypeError(
                f"{SkillConversation.__name__}.conversation_id should not be None"
            )

        if not self.service_url:
            raise TypeError(
                f"{SkillConversation.__name__}.service_url should not be None"
            )

        json_str = json.dumps([self.conversation_id, self.service_url])
        return str(base64.b64encode(json_str.encode("utf-8")), "utf-8")
