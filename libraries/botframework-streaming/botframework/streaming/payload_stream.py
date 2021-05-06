# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from asyncio import Lock, Semaphore
from typing import List

from botframework.streaming.payloads.assemblers import PayloadStreamAssembler


class PayloadStream:
    def __init__(self, assembler: PayloadStreamAssembler):
        self._assembler = assembler
        self._buffer_queue: List[List[int]] = []
        self._lock = Lock()
        self._data_available = Semaphore(0)
        self._producer_length = 0  # total length
        self._consumer_position = 0  # read position
        self._active: List[int] = []
        self._active_offset = 0
        self._end = False

    def __len__(self):
        return self._producer_length

    def give_buffer(self, buffer: List[int]):
        self._buffer_queue.append(buffer)
        self._producer_length += len(buffer)

        self._data_available.release()

    def done_producing(self):
        self.give_buffer([])

    def write(self, buffer: List[int], offset: int, count: int):
        buffer_copy = buffer[offset : offset + count]
        self.give_buffer(buffer_copy)

    async def read(self, buffer: List[int], offset: int, count: int):
        if self._end:
            return 0

        if not self._active:
            await self._data_available.acquire()
            async with self._lock:
                self._active = self._buffer_queue.pop(0)

        available_count = min(len(self._active) - self._active_offset, count)

        for index in range(available_count):
            buffer[offset + index] = self._active[self._active_offset]
            self._active_offset += 1

        self._consumer_position += available_count

        if self._active_offset >= len(self._active):
            self._active = []
            self._active_offset = 0

        if (
            self._assembler
            and self._consumer_position >= self._assembler.content_length
        ):
            self._end = True

        return available_count

    async def read_until_end(self):
        result = [None] * self._assembler.content_length
        current_size = 0

        while not self._end:
            count = await self.read(
                result, current_size, self._assembler.content_length
            )
            current_size += count

        return result
