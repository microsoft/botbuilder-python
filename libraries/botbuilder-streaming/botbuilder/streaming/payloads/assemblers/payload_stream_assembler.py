# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import UUID
from typing import List
from threading import Lock

import botbuilder.streaming as streaming
import botbuilder.streaming.payloads as payloads
from botbuilder.streaming.payloads.models import Header

from .assembler import Assembler


class PayloadStreamAssembler(Assembler):
    def __init__(
        self,
        stream_manager: "payloads.StreamManager",
        identifier: UUID,
        type: str = None,
        length: int = None,
    ):

        self._stream_manager = stream_manager or payloads.StreamManager()
        self._stream: "streaming.PayloadStream" = None
        self._lock = Lock()
        self.identifier = identifier
        self.content_type = type
        self.content_length = length
        self.end: bool = None

    def create_stream_from_payload(self) -> "streaming.PayloadStream":
        return streaming.PayloadStream(self)

    def get_payload_as_stream(self) -> "streaming.PayloadStream":
        with self._lock:
            if not self._stream:
                self._stream = self.create_stream_from_payload()

        return self._stream

    def on_receive(self, header: Header, stream: List[int], content_length: int):
        if header.end:
            self.end = True
            self._stream.done_producing()

    def close(self):
        self._stream_manager.close_stream(self.identifier)
