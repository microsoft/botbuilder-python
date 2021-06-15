# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List, Union, Type

from msrest.serialization import Model
from botframework.streaming.payloads import ContentStream
from botframework.streaming.payloads.models import Serializable


class ReceiveResponse:
    def __init__(self, status_code: int = 0, streams: List[ContentStream] = None):
        self.status_code = status_code
        self.streams = streams or []

    def read_body_as_json(
        self, cls: Union[Type[Model], Type[Serializable]]
    ) -> Union[Model, Serializable]:
        try:
            body_str = self.read_body_as_str()
            body = None

            if issubclass(cls, Serializable):
                body = cls().from_json(body_str)
            elif isinstance(cls, Model):
                body = cls.deserialize(body_str)
            return body
        except Exception as error:
            raise error

    def read_body_as_str(self) -> str:
        try:
            content_stream = self.read_body()

            if not content_stream:
                return ""

            # TODO: encoding double check
            return content_stream.decode("utf8")
        except Exception as error:
            raise error

    def read_body(self) -> bytes:
        try:
            content_stream = self.streams[0] if self.streams else None

            if not content_stream:
                return None

            return bytes(content_stream.stream)
        except Exception as error:
            raise error
