# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
from typing import List

from .serializable import Serializable
from .stream_description import StreamDescription


class ResponsePayload(Serializable):
    def __init__(
        self, *, status_code: int = None, streams: List[StreamDescription] = None
    ):
        self.status_code = status_code
        self.streams = streams

    def to_json(self) -> str:
        obj = {"statusCode": self.status_code}

        if self.streams:
            obj["streams"] = [stream.to_dict() for stream in self.streams]

        return json.dumps(obj)

    def from_json(self, json_str: str) -> "ResponsePayload":
        obj = json.loads(json_str)

        self.status_code = obj.get("statusCode")
        stream_list = obj.get("streams")

        if stream_list:
            self.streams = [
                StreamDescription().from_dict(stream_dict)
                for stream_dict in stream_list
            ]

        return self
