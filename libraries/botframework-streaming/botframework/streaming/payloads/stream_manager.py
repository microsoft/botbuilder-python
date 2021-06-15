# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import UUID
from typing import Callable, Dict, List

from botframework.streaming.payloads.assemblers import PayloadStreamAssembler
from botframework.streaming.payloads.models import Header


class StreamManager:
    def __init__(
        self, on_cancel_stream: Callable[[PayloadStreamAssembler], None] = None
    ):
        self._on_cancel_stream = on_cancel_stream or (lambda ocs: None)
        self._active_assemblers: Dict[UUID, PayloadStreamAssembler] = {}

    def get_payload_assembler(self, identifier: UUID) -> PayloadStreamAssembler:
        self._active_assemblers[identifier] = self._active_assemblers.get(
            identifier, PayloadStreamAssembler(self, identifier)
        )

        return self._active_assemblers[identifier]

    def get_payload_stream(self, header: Header) -> "streaming.PayloadStream":
        assembler = self.get_payload_assembler(header.id)

        return assembler.get_payload_as_stream()

    def on_receive(
        self, header: Header, content_stream: List[int], content_length: int
    ):
        assembler = self._active_assemblers.get(header.id)

        if assembler:
            assembler.on_receive(header, content_stream, content_length)

    def close_stream(self, identifier: UUID):
        assembler = self._active_assemblers.get(identifier)

        if assembler:
            del self._active_assemblers[identifier]
            stream = assembler.get_payload_as_stream()
            if (
                assembler.content_length
                and len(stream) < assembler.content_length
                or not assembler.end
            ):
                self._on_cancel_stream(assembler)
