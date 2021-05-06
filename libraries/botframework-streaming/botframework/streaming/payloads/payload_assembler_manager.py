# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import UUID
from typing import Awaitable, Callable, Dict, List, Union

from botframework.streaming.payloads.assemblers import (
    Assembler,
    ReceiveRequestAssembler,
    ReceiveResponseAssembler,
)
from botframework.streaming.payloads.models import Header, PayloadTypes

from .stream_manager import StreamManager


class PayloadAssemblerManager:
    def __init__(
        self,
        stream_manager: StreamManager,
        on_receive_request: Callable[[UUID, "streaming.ReceiveRequest"], Awaitable],
        on_receive_response: Callable[[UUID, "streaming.ReceiveResponse"], Awaitable],
    ):
        self._on_receive_request = on_receive_request
        self._on_receive_response = on_receive_response
        self._stream_manager = stream_manager
        self._active_assemblers: Dict[UUID, Assembler] = {}

    def get_payload_stream(
        self, header: Header
    ) -> Union[List[int], "streaming.PayloadStream"]:
        # TODO: The return value SHOULDN'T be a union, we should interface List[int] into a BFStream class
        if self._is_stream_payload(header):
            return self._stream_manager.get_payload_stream(header)
        if not self._active_assemblers.get(header.id):
            # a new requestId has come in, start a new task to process it as it is received
            assembler = self._create_payload_assembler(header)
            if assembler:
                self._active_assemblers[header.id] = assembler
                return assembler.get_payload_as_stream()

        return None

    def on_receive(
        self, header: Header, content_stream: List[int], content_length: int
    ):
        if self._is_stream_payload(header):
            self._stream_manager.on_receive(header, content_stream, content_length)
        else:
            assembler = self._active_assemblers.get(header.id)
            if assembler:
                assembler.on_receive(header, content_stream, content_length)

                # remove them when we are done
                if header.end:
                    del self._active_assemblers[header.id]

            # ignore unknown header ids

    def _create_payload_assembler(self, header: Header) -> Assembler:
        if header.type == PayloadTypes.REQUEST:
            return ReceiveRequestAssembler(
                header, self._stream_manager, self._on_receive_request
            )
        if header.type == PayloadTypes.RESPONSE:
            return ReceiveResponseAssembler(
                header, self._stream_manager, self._on_receive_response
            )

        return None

    def _is_stream_payload(self, header: Header) -> bool:
        return PayloadTypes.is_stream(header)
