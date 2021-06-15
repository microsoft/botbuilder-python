# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
from typing import List

from .serializable import Serializable
from .stream_description import StreamDescription


class RequestPayload(Serializable):
    def __init__(
        self,
        *,
        verb: str = None,
        path: str = None,
        streams: List[StreamDescription] = None
    ):
        self.verb = verb
        self.path = path
        self.streams = streams

    def to_json(self) -> str:
        obj = {"verb": self.verb, "path": self.path}

        if self.streams:
            obj["streams"] = [stream.to_dict() for stream in self.streams]

        return json.dumps(obj)

    def from_json(self, json_str: str) -> "RequestPayload":
        obj = json.loads(json_str)

        self.verb = obj.get("verb")
        self.path = obj.get("path")
        stream_list = obj.get("streams")

        if stream_list:
            self.streams = [
                StreamDescription().from_dict(stream_dict)
                for stream_dict in stream_list
            ]

        return self
