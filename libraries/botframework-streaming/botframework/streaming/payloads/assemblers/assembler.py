# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


from abc import ABC
from uuid import UUID

from typing import List

from botframework.streaming.payloads.models import Header


class Assembler(ABC):
    def __init__(self, end: bool, identifier: UUID):
        self.end = end
        self.identifier = identifier

    def close(self):
        raise NotImplementedError()

    def create_stream_from_payload(self) -> List[int]:
        raise NotImplementedError()

    def get_payload_as_stream(self) -> List[int]:
        raise NotImplementedError()

    def on_receive(
        self, header: Header, stream: List[int], content_length: int
    ) -> List[int]:
        raise NotImplementedError()
