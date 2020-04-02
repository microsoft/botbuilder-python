# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import UUID, uuid4
from typing import List

from botbuilder.streaming.payloads import ResponseMessageStream


class StreamingRequest:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    def __init__(
        self,
        *,
        verb: str = None,
        path: str = None,
        streams: List[ResponseMessageStream] = None
    ):
        self.verb = verb
        self.path = path
        self.streams = streams

    @staticmethod
    def create_request(
        method: str, path: str = None, body: object = None
    ) -> "StreamingRequest":
        if not method:
            return None

        request = StreamingRequest(verb=method, path=path,)

        if body:
            request.add_stream(body)

        return request

    @staticmethod
    def create_get(path: str = None, body: object = None) -> "StreamingRequest":
        return StreamingRequest.create_request("GET", path, body)

    @staticmethod
    def create_post(path: str = None, body: object = None) -> "StreamingRequest":
        return StreamingRequest.create_request("POST", path, body)

    @staticmethod
    def create_put(path: str = None, body: object = None) -> "StreamingRequest":
        return StreamingRequest.create_request("PUT", path, body)

    @staticmethod
    def create_delete(path: str = None, body: object = None) -> "StreamingRequest":
        return StreamingRequest.create_request("DELETE", path, body)

    def add_stream(self, content: object, stream_id: UUID = None):
        if not content:
            raise TypeError("'content' argument can not be None")
        if not self.streams:
            self.streams = []

        self.streams.append(
            ResponseMessageStream(id=stream_id or uuid4(), content=content)
        )
