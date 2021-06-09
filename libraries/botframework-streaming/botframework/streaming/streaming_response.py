# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
from http import HTTPStatus
from uuid import UUID, uuid4
from typing import List, Union

from msrest.serialization import Model
from botframework.streaming.payloads import ResponseMessageStream
from botframework.streaming.payloads.models import Serializable


class StreamingResponse:
    def __init__(
        self, *, status_code: int = 0, streams: List[ResponseMessageStream] = None
    ):
        self.status_code = status_code
        self.streams = streams

    def add_stream(self, content: object, identifier: UUID = None):
        if not content:
            raise TypeError("content can't be None")

        if self.streams is None:
            self.streams: List[ResponseMessageStream] = []

        self.streams.append(
            ResponseMessageStream(id=identifier or uuid4(), content=content)
        )

    def set_body(self, body: Union[str, Serializable, Model]):
        # TODO: verify if msrest.serialization.Model is necessary
        if not body:
            return

        if isinstance(body, Serializable):
            body = body.to_json()
        elif isinstance(body, Model):
            body = json.dumps(body.as_dict())

        self.add_stream(list(body.encode()))

    @staticmethod
    def create_response(status_code: int, body: object) -> "StreamingResponse":
        response = StreamingResponse(status_code=status_code)

        if body:
            response.add_stream(body)

        return response

    @staticmethod
    def not_found(body: object = None) -> "StreamingResponse":
        return StreamingResponse.create_response(HTTPStatus.NOT_FOUND, body)

    @staticmethod
    def forbidden(body: object = None) -> "StreamingResponse":
        return StreamingResponse.create_response(HTTPStatus.FORBIDDEN, body)

    # pylint: disable=invalid-name
    @staticmethod
    def ok(body: object = None) -> "StreamingResponse":
        return StreamingResponse.create_response(HTTPStatus.OK, body)

    @staticmethod
    def internal_server_error(body: object = None) -> "StreamingResponse":
        return StreamingResponse.create_response(HTTPStatus.INTERNAL_SERVER_ERROR, body)
