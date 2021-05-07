# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
from uuid import UUID
from typing import Awaitable, Callable, List

import botframework.streaming as streaming
import botframework.streaming.payloads as payloads
from botframework.streaming.payloads.models import Header, ResponsePayload

from .assembler import Assembler


class ReceiveResponseAssembler(Assembler):
    # pylint: disable=super-init-not-called
    def __init__(
        self,
        header: Header,
        stream_manager: "payloads.StreamManager",
        on_completed: Callable[[UUID, "streaming.ReceiveResponse"], Awaitable],
    ):
        if not header:
            raise TypeError(
                f"'header: {header.__class__.__name__}' argument can't be None"
            )
        if not on_completed:
            raise TypeError(f"'on_completed' argument can't be None")

        self._stream_manager = stream_manager
        self._on_completed = on_completed
        self.identifier = header.id
        self._length = header.payload_length if header.end else None
        self._stream: List[int] = None

    def create_stream_from_payload(self) -> List[int]:
        return [None] * (self._length or 0)

    def get_payload_as_stream(self) -> List[int]:
        if self._stream is None:
            self._stream = self.create_stream_from_payload()

        return self._stream

    def on_receive(self, header: Header, stream: List[int], content_length: int):
        if header.end:
            self.end = header.end

            # Execute the response on a separate Task
            # Execute the request on a separate Thread in the background
            # Execute the request on a separate in the background
            asyncio.ensure_future(self.process_response(stream))

    def close(self):
        self._stream_manager.close_stream(self.identifier)

    async def process_response(self, stream: List[int]):
        response_payload = ResponsePayload().from_json(bytes(stream).decode("utf8"))

        response = streaming.ReceiveResponse(
            status_code=response_payload.status_code, streams=[]
        )

        if response_payload.streams:
            for stream_description in response_payload.streams:
                try:
                    identifier = UUID(int=int(stream_description.id))
                except Exception:
                    raise ValueError(
                        f"Stream description id '{stream_description.id}' is not a Guid"
                    )

                stream_assembler = self._stream_manager.get_payload_assembler(
                    identifier
                )
                stream_assembler.content_type = stream_description.content_type
                stream_assembler.content_length = stream_description.length

                content_stream = payloads.ContentStream(
                    identifier=identifier, assembler=stream_assembler
                )
                content_stream.length = stream_description.length
                content_stream.content_type = stream_description.content_type
                response.streams.append(content_stream)

        await self._on_completed(self.identifier, response)
