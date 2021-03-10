# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json

from .serializable import Serializable


class StreamDescription(Serializable):
    # pylint: disable=invalid-name
    def __init__(self, *, id: str = None, content_type: str = None, length: int = None):
        self.id = id
        self.content_type = content_type
        self.length = length

    def to_dict(self) -> dict:
        obj = {"id": self.id, "type": self.content_type}

        if self.length is not None:
            obj["length"] = self.length

        return obj

    def from_dict(self, json_dict: dict) -> "StreamDescription":
        self.id = json_dict.get("id")
        self.content_type = json_dict.get("type")
        self.length = json_dict.get("length")

        return self

    def to_json(self) -> str:
        return json.dumps(self.to_dict)

    def from_json(self, json_str: str) -> "StreamDescription":
        obj = json.loads(json_str)
        return self.from_dict(obj)
