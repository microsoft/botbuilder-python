# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import traceback

from asyncio import iscoroutinefunction, isfuture
from typing import Callable, List

import botframework.streaming as streaming
from botframework.streaming.payloads import HeaderSerializer
from botframework.streaming.payloads.models import Header, PayloadTypes
from botframework.streaming.transport import (
    DisconnectedEventArgs,
    TransportConstants,
    TransportReceiverBase,
)


class PayloadReceiver:
    def __init__(self):
        self._get_stream: Callable[[Header], List[int]] = None
        self._receive_action: Callable[[Header, List[int], int], None] = None
        self._receiver: TransportReceiverBase = None
        self._is_disconnecting = False

        self._receive_header_buffer: List[int] = [
            None
        ] * TransportConstants.MAX_HEADER_LENGTH
        self._receive_content_buffer: List[int] = [
            None
        ] * TransportConstants.MAX_PAYLOAD_LENGTH

        self.disconnected: Callable[[object, DisconnectedEventArgs], None] = None

    @property
    def is_connected(self) -> bool:
        return self._receiver is not None

    async def connect(self, receiver: TransportReceiverBase):
        if self._receiver:
            raise RuntimeError(f"{self.__class__.__name__} instance already connected.")

        self._receiver = receiver
        await self._run_receive()

    async def _run_receive(self):
        await self._receive_packets()

    def subscribe(
        self,
        get_stream: Callable[[Header], List[int]],
        receive_action: Callable[[Header, List[int]], int],
    ):
        self._get_stream = get_stream
        self._receive_action = receive_action

    async def disconnect(self, event_args: DisconnectedEventArgs = None):
        did_disconnect = False

        if not self._is_disconnecting:
            self._is_disconnecting = True
            try:
                try:
                    if self._receiver:
                        await self._receiver.close()
                        # TODO: investigate if 'dispose' is necessary
                        did_disconnect = True
                except Exception:
                    traceback.print_exc()

                self._receiver = None

                if did_disconnect:
                    if callable(self.disconnected):
                        # pylint: disable=not-callable
                        if iscoroutinefunction(self.disconnected) or isfuture(
                            self.disconnected
                        ):
                            await self.disconnected(
                                self, event_args or DisconnectedEventArgs.empty
                            )
                        else:
                            self.disconnected(
                                self, event_args or DisconnectedEventArgs.empty
                            )
            finally:
                self._is_disconnecting = False

    async def _receive_packets(self):
        is_closed = False
        disconnect_args = None

        while self._receiver and self._receiver.is_connected and not is_closed:
            # receive a single packet
            try:
                # read the header
                header_offset = 0
                # TODO: this while is probalby not necessary
                while header_offset < TransportConstants.MAX_HEADER_LENGTH:
                    length = await self._receiver.receive(
                        self._receive_header_buffer,
                        header_offset,
                        TransportConstants.MAX_HEADER_LENGTH - header_offset,
                    )

                    if length == 0:
                        # TODO: make custom exception
                        raise Exception(
                            "TransportDisconnectedException: Stream closed while reading header bytes"
                        )

                    header_offset += length

                # deserialize the bytes into a header
                header = HeaderSerializer.deserialize(
                    self._receive_header_buffer, 0, TransportConstants.MAX_HEADER_LENGTH
                )

                # read the payload
                content_stream = self._get_stream(header)

                buffer = (
                    [None] * header.payload_length
                    if PayloadTypes.is_stream(header)
                    else self._receive_content_buffer
                )
                offset = 0

                if header.payload_length:
                    while offset < header.payload_length:
                        count = min(
                            header.payload_length - offset,
                            TransportConstants.MAX_PAYLOAD_LENGTH,
                        )

                        # Send: Packet content
                        length = await self._receiver.receive(buffer, offset, count)
                        if length == 0:
                            # TODO: make custom exception
                            raise Exception(
                                "TransportDisconnectedException: Stream closed while reading header bytes"
                            )

                        if content_stream is not None:
                            # write chunks to the content_stream if it's not a stream type
                            # TODO: this has to be improved in custom buffer class (validate buffer ended)
                            if not PayloadTypes.is_stream(header):
                                for index in range(offset, offset + length):
                                    content_stream[index] = buffer[index]

                        offset += length

                    # give the full payload buffer to the contentStream if it's a stream
                    if PayloadTypes.is_stream(header) and isinstance(
                        content_stream, streaming.PayloadStream
                    ):
                        content_stream.give_buffer(buffer)

                    self._receive_action(header, content_stream, offset)
            except Exception as exception:
                traceback.print_exc()
                is_closed = True
                disconnect_args = DisconnectedEventArgs(reason=str(exception))

        await self.disconnect(disconnect_args)
