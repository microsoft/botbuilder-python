# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import UUID
from typing import List
from threading import Lock

from botbuilder.streaming.payloads.models import Header

from .assembler import Assembler


class PayloadStreamAssembler(Assembler):
    def __init__(
        self,
        stream_manager: "StreamManager",
        identifier: UUID,
        type: str = None,
        length: int = None,
    ):
        from botbuilder.streaming.payloads import StreamManager

        self._stream_manager = stream_manager or StreamManager()
        self._stream: List[int] = []
        self._lock = Lock()
        self.identifier = identifier
        self.content_type = type
        self.content_length = length
        self.end: bool = None

    # TODO: highly probable this can be removed
    def create_stream_from_payload(self) -> List[int]:
        return []

    # TODO: somewhat probable this can be removed
    def get_payload_as_stream(self) -> List[int]:
        with self._lock:
            if self._stream is None:
                self._stream = self.create_stream_from_payload()

        return self._stream

    def on_receive(
        self, header: Header, stream: List[int], content_length: int
    ) -> List[int]:
        if header.end:
            self.end = True

    def close(self):
        self._stream_manager.close_stream(self.identifier)
