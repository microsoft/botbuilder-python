# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
from asyncio import Future
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List

from botframework.streaming.transport import TransportConstants
from botframework.streaming.payload_transport import PayloadSender
from botframework.streaming.payloads import ResponseMessageStream
from botframework.streaming.payloads.models import (
    Header,
    Serializable,
    StreamDescription,
)


class PayloadDisassembler(ABC):
    def __init__(self, sender: PayloadSender, identifier: UUID):
        self.sender = sender
        self.identifier = identifier
        self._task_completion_source = Future()

        self._stream: List[int] = None
        self._stream_length: int = None
        self._send_offset: int = None
        self._is_end: bool = False
        self._type: str = None

    @property
    @abstractmethod
    def type(self) -> str:
        return self._type

    async def get_stream(self) -> List[int]:
        raise NotImplementedError()

    async def disassemble(self):
        self._stream = await self.get_stream()
        self._stream_length = len(self._stream)
        self._send_offset = 0

        await self._send()

    @staticmethod
    def get_stream_description(stream: ResponseMessageStream) -> StreamDescription:
        description = StreamDescription(id=str(stream.id))

        # TODO: This content type is hardcoded for POC, investigate how to proceed
        content = bytes(stream.content).decode("utf8")

        try:
            json.loads(content)
            content_type = "application/json"
        except ValueError:
            content_type = "text/plain"

        description.content_type = content_type
        description.length = len(content)

        # TODO: validate statement below, also make the string a constant
        # content_length: int = stream.content.headers.get("Content-Length")
        # if content_length:
        #     description.length = int(content_length)
        # else:
        #     # TODO: check statement validity
        #     description.length = stream.content.headers.content_length

        return description

    @staticmethod
    def serialize(item: Serializable, stream: List[int], length: List[int]):
        encoded_json = item.to_json().encode()
        stream.clear()
        stream.extend(list(encoded_json))

        length.clear()
        length.append(len(stream))

    async def _send(self):
        # determine if we know the length we can send and whether we can tell if this is the end
        is_length_known = self._is_end

        header = Header(type=self.type, id=self.identifier, end=self._is_end)

        header.payload_length = 0

        if self._stream_length is not None:
            # determine how many bytes we can send and if we are at the end
            header.payload_length = min(
                self._stream_length - self._send_offset,
                TransportConstants.MAX_PAYLOAD_LENGTH,
            )
            header.end = (
                self._send_offset + header.payload_length >= self._stream_length
            )
            is_length_known = True

        self.sender.send_payload(header, self._stream, is_length_known, self._on_send)

    async def _on_send(self, header: Header):
        self._send_offset += header.payload_length
        self._is_end = header.end

        if self._is_end:
            self._task_completion_source.set_result(True)
        else:
            await self._send()
