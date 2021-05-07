# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import UUID
from typing import List

from botframework.streaming.payload_transport import PayloadSender
from botframework.streaming.payloads.models import PayloadTypes, ResponsePayload

from .payload_disassembler import PayloadDisassembler


class ResponseDisassembler(PayloadDisassembler):
    def __init__(
        self,
        sender: PayloadSender,
        identifier: UUID,
        response: "streaming.StreamingResponse",
    ):
        super().__init__(sender, identifier)

        self.response = response

    @property
    def type(self) -> str:
        return PayloadTypes.RESPONSE

    async def get_stream(self) -> List[int]:
        payload = ResponsePayload(status_code=self.response.status_code)

        if self.response.streams:
            payload.streams = [
                self.get_stream_description(content_stream)
                for content_stream in self.response.streams
            ]

        memory_stream: List[int] = []
        stream_length: List[int] = []
        # TODO: high probability stream length is not necessary
        self.serialize(payload, memory_stream, stream_length)

        return memory_stream
