# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
from uuid import UUID

from botframework.streaming.payload_transport import PayloadSender
from botframework.streaming.payloads.disassemblers import (
    CancelDisassembler,
    RequestDisassembler,
    ResponseDisassembler,
    ResponseMessageStreamDisassembler,
)
from botframework.streaming.payloads.models import PayloadTypes


class SendOperations:
    def __init__(self, payload_sender: PayloadSender):
        self._payload_sender = payload_sender

    async def send_request(
        self, identifier: UUID, request: "streaming.StreamingRequest"
    ):
        disassembler = RequestDisassembler(self._payload_sender, identifier, request)

        await disassembler.disassemble()

        if request.streams:
            tasks = [
                ResponseMessageStreamDisassembler(
                    self._payload_sender, content_stream
                ).disassemble()
                for content_stream in request.streams
            ]

            await asyncio.gather(*tasks)

    async def send_response(
        self, identifier: UUID, response: "streaming.StreamingResponse"
    ):
        disassembler = ResponseDisassembler(self._payload_sender, identifier, response)

        await disassembler.disassemble()

        if response.streams:
            tasks = [
                ResponseMessageStreamDisassembler(
                    self._payload_sender, content_stream
                ).disassemble()
                for content_stream in response.streams
            ]

            await asyncio.gather(*tasks)

    async def send_cancel_all(self, identifier: UUID):
        disassembler = CancelDisassembler(
            sender=self._payload_sender,
            identifier=identifier,
            type=PayloadTypes.CANCEL_ALL,
        )

        await disassembler.disassemble()

    async def send_cancel_stream(self, identifier: UUID):
        disassembler = CancelDisassembler(
            sender=self._payload_sender,
            identifier=identifier,
            type=PayloadTypes.CANCEL_STREAM,
        )

        await disassembler.disassemble()
