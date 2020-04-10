# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List, Union, Type

from msrest.serialization import Model
from botbuilder.streaming.payloads import ContentStream
from botbuilder.streaming.payloads.models import Serializable


class ReceiveResponse:
    def __init__(self, status_code: int = None, streams: List[ContentStream] = None):
        self.status_code = status_code
        self.streams = streams

    def read_body_as_json(
        self, cls: Type[Model, Serializable]
    ) -> Union[Model, Serializable]:
        try:
            body_str = self.read_body_as_str()

            if issubclass(cls, Serializable):
                body = cls().from_json(body_str)
            elif isinstance(cls, Model):
                body = cls.deserialize(body_str)
            return body
        except Exception as error:
            raise error

    def read_body_as_str(self) -> str:
        try:
            content_stream = self.streams[0] if self.streams else None

            if not content_stream:
                return ""

            return bytes(content_stream.stream).decode("utf8")
        except Exception as error:
            raise error
