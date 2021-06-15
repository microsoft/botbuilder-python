# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from asyncio import Event, ensure_future, iscoroutinefunction, isfuture
from typing import Awaitable, Callable, List

from botframework.streaming.transport import (
    DisconnectedEventArgs,
    TransportSenderBase,
    TransportConstants,
)
from botframework.streaming.payloads import HeaderSerializer
from botframework.streaming.payloads.models import Header

from .send_queue import SendQueue
from .send_packet import SendPacket


# TODO: consider interface this class
class PayloadSender:
    def __init__(self):
        self._connected_event = Event()
        self._sender: TransportSenderBase = None
        self._is_disconnecting: bool = False
        self._send_header_buffer: List[int] = [
            None
        ] * TransportConstants.MAX_HEADER_LENGTH
        self._send_content_buffer: List[int] = [
            None
        ] * TransportConstants.MAX_PAYLOAD_LENGTH

        self._send_queue = SendQueue(action=self._write_packet)

        self.disconnected: Callable[[object, DisconnectedEventArgs], None] = None

    @property
    def is_connected(self) -> bool:
        return self._sender is not None

    def connect(self, sender: TransportSenderBase):
        if self._sender:
            raise RuntimeError(f"{self.__class__.__name__} instance already connected.")

        self._sender = sender
        self._connected_event.set()

    # TODO: check 'stream' for payload
    def send_payload(
        self,
        header: Header,
        payload: object,
        is_length_known: bool,
        sent_callback: Callable[[Header], Awaitable],
    ):
        packet = SendPacket(
            header=header,
            payload=payload,
            is_length_known=is_length_known,
            sent_callback=sent_callback,
        )

        self._send_queue.post(packet)

    async def disconnect(self, event_args: DisconnectedEventArgs = None):
        did_disconnect = False

        if not self._is_disconnecting:
            self._is_disconnecting = True
            try:
                try:
                    if self._sender:
                        self._sender.close()
                        # TODO: investigate if 'dispose' is necessary
                        did_disconnect = True
                except Exception:
                    pass

                self._sender = None

                if did_disconnect:
                    self._connected_event.clear()
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

    async def _write_packet(self, packet: SendPacket):
        await self._connected_event.wait()

        try:
            # determine if we know the payload length and end
            if not packet.is_length_known:
                count = packet.header.payload_length
                packet.header.end = count == 0

            header_length = HeaderSerializer.serialize(
                packet.header, self._send_header_buffer, 0
            )

            # Send: Packet Header
            length = await self._sender.send(self._send_header_buffer, 0, header_length)
            if not length:
                # TODO: make custom exception
                raise Exception("TransportDisconnectedException")

            offset = 0

            # Send content in chunks
            if packet.header.payload_length and packet.payload:
                # If we already read the buffer, send that
                # If we did not, read from the stream until we've sent that amount
                if not packet.is_length_known:
                    # Send: Packet content
                    length = await self._sender.send(
                        self._send_content_buffer, 0, packet.header.payload_length
                    )
                    if length == 0:
                        # TODO: make custom exception
                        raise Exception("TransportDisconnectedException")
                else:
                    while offset < packet.header.payload_length:
                        count = min(
                            packet.header.payload_length - offset,
                            TransportConstants.MAX_PAYLOAD_LENGTH,
                        )

                        # copy the stream to the buffer
                        # TODO: this has to be improved in custom buffer class (validate buffer ended)
                        for index in range(count):
                            self._send_content_buffer[index] = packet.payload[index]

                        # Send: Packet content
                        length = await self._sender.send(
                            self._send_content_buffer, 0, count
                        )
                        if length == 0:
                            # TODO: make custom exception
                            raise Exception("TransportDisconnectedException")

                        offset += count

            if packet.sent_callback:
                # TODO: should this really run in the background?
                ensure_future(packet.sent_callback(packet.header))
        except Exception as exception:
            disconnected_args = DisconnectedEventArgs(reason=str(exception))
            await self.disconnect(disconnected_args)
