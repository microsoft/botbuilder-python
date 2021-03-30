# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import UUID

from botbuilder.streaming.payload_transport import PayloadSender
from botbuilder.streaming.payloads.models import Header


class CancelDisassembler:
    def __init__(self, *, sender: PayloadSender, identifier: UUID, type: str):
        self._sender = sender
        self._identifier = identifier
        self._type = type

    async def disassemble(self):
        header = Header(type=self._type, id=self._identifier, end=True)

        header.payload_length = 0

        self._sender.send_payload(header, None, True, None)
        return
