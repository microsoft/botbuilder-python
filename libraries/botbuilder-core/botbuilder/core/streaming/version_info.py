# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json

from botframework.streaming.payloads.models import Serializable


class VersionInfo(Serializable):
    def __init__(self, *, user_agent: str = None):
        self.user_agent = user_agent

    def to_json(self) -> str:
        obj = {"userAgent": self.user_agent}

        return json.dumps(obj)

    def from_json(self, json_str: str) -> "ResponsePayload":
        obj = json.loads(json_str)

        self.user_agent = obj.get("userAgent")
        return self
