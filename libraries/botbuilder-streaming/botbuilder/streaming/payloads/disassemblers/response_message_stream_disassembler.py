# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.streaming.payload_transport import PayloadSender
from botbuilder.streaming.payloads import ResponseMessageStream
from botbuilder.streaming.payloads.models import PayloadTypes

from .payload_disassembler import PayloadDisassembler


class ResponseMessageStreamDisassembler(PayloadDisassembler):
    def __init__(self, sender: PayloadSender, content_stream: ResponseMessageStream):
        super().__init__(sender, content_stream.id)

        self.content_stream = content_stream

    @property
    def type(self) -> str:
        return PayloadTypes.REQUEST

    async def get_stream(self) -> List[int]:
        # TODO: align logic below to the shape of content_stream.content
        stream: List[int] = list(str(self.content_stream.content).encode())

        return stream
