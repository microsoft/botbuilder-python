# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import UUID

from botbuilder.streaming import StreamingRequest
from botbuilder.streaming.payload_transport import PayloadSender


class SendOperations:
    def __init__(self, payload_sender: PayloadSender):
        self._payload_sender = payload_sender

    async def send_request(self, identifier: UUID, request: StreamingRequest):
        disassembler
