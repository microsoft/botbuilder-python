# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import UUID
from typing import List

from botframework.streaming.payload_transport import PayloadSender
from botframework.streaming.payloads.models import PayloadTypes, RequestPayload

from .payload_disassembler import PayloadDisassembler


class RequestDisassembler(PayloadDisassembler):
    def __init__(
        self,
        sender: PayloadSender,
        identifier: UUID,
        request: "streaming.StreamingRequest",
    ):
        super().__init__(sender, identifier)

        self.request = request

    @property
    def type(self) -> str:
        return PayloadTypes.REQUEST

    async def get_stream(self) -> List[int]:
        payload = RequestPayload(verb=self.request.verb, path=self.request.path)

        if self.request.streams:
            payload.streams = [
                self.get_stream_description(content_stream)
                for content_stream in self.request.streams
            ]

        memory_stream: List[int] = []
        stream_length: List[int] = []
        # TODO: high probability stream length is not necessary
        self.serialize(payload, memory_stream, stream_length)

        return memory_stream
