# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import uuid4
from typing import Dict, Tuple


class RoutingIdFactory:
    def __init__(self):
        self._forward_x_ref: Dict[str, str] = {}
        self._backward_x_ref: Dict[str, Tuple[str, str]] = {}

    def create_skill_conversation_id(self, conversation_id: str, service_url: str) -> str:
        result = self._forward_x_ref.get(conversation_id, str(uuid4()))

        self._forward_x_ref[conversation_id] = result
        self._backward_x_ref[result] = (conversation_id, service_url)

        return result

    def get_conversation_info(self, encoded_conversation_id) -> Tuple[str, str]:
        return self._backward_x_ref[encoded_conversation_id]
