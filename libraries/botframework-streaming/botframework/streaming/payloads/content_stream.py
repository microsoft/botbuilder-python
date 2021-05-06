# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import UUID

from botframework.streaming.payloads.assemblers import PayloadStreamAssembler


class ContentStream:
    def __init__(self, identifier: UUID, assembler: PayloadStreamAssembler):
        if not assembler:
            raise TypeError(
                f"'assembler: {assembler.__class__.__name__}' argument can't be None"
            )

        self.identifier = identifier
        self._assembler = assembler
        self.stream = self._assembler.get_payload_as_stream()
        self.content_type: str = None
        self.length: int = None

    def cancel(self):
        self._assembler.close()
