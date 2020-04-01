# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

# TODO: reconsider to absolute import
from .payloads import ResponseMessageStream


class StreamingResponse:
    def __init__(
        self, *, status_code: int = None, streams: List[ResponseMessageStream] = None
    ):
        self.status_code = status_code
        self.streams = streams

    def add_stream(self, content: object):
        if not content:
            raise TypeError("content can't be None")

        if self.streams is None:
            self.streams: List[ResponseMessageStream] = []

        self.streams.append(ResponseMessageStream(content=content))

    @staticmethod
    def create_response(status_code: int, body: object) -> "StreamingResponse":
        response = StreamingResponse(status_code=status_code)

        if body:
            response.add_stream(body)

        return response
