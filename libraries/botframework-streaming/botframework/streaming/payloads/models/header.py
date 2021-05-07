# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import UUID

from botframework.streaming.transport import TransportConstants


class Header:
    # pylint: disable=invalid-name
    def __init__(self, *, type: str = None, id: UUID = None, end: bool = None):
        self._internal_payload_length = None
        self.type: str = type
        self.id: UUID = id
        self.end: bool = end

    @property
    def payload_length(self) -> int:
        return self._internal_payload_length

    @payload_length.setter
    def payload_length(self, value: int):
        self._validate_length(
            value, TransportConstants.MAX_LENGTH, TransportConstants.MIN_LENGTH
        )
        self._internal_payload_length = value

    def _validate_length(self, value: int, max_val: int, min_val: int):
        if value > max_val:
            raise ValueError(f"Length must be less or equal than {max_val}")

        if value < min_val:
            raise ValueError(f"Length must be greater or equal than {min_val}")
