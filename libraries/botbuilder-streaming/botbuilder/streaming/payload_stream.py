# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from threading import Lock
from typing import List

from botbuilder.streaming.payloads.assemblers import PayloadStreamAssembler


class PayloadStream:
    def __init__(self, assembler: PayloadStreamAssembler):
        self._assembler = assembler
        self._buffer_queue: List[int] = []
        self._lock = Lock()
        self._producer_length = 0  # total length
        self._consumer_length = 0  # read position
        self._active: List[int] = []
        self._active_offset = 0
        self._end = False
