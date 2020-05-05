# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.streaming.transport import TransportReceiverBase, TransportSenderBase

from .web_socket import WebSocket
from .web_socket_message_type import WebSocketMessageType
from .web_socket_close_status import WebSocketCloseStatus
from .web_socket_state import WebSocketState


class WebSocketTransport(TransportReceiverBase, TransportSenderBase):
    def __init__(self, web_socket: WebSocket):
        self._socket = web_socket

    @property
    def is_connected(self):
        print("Getting value")
        # TODO: mock logic
        return self._socket.status == WebSocketState.OPEN

    async def close(self):
        # TODO: mock logic
        if self._socket.status == WebSocketState.OPEN:
            try:
                await self._socket.close(
                    WebSocketCloseStatus.NORMAL_CLOSURE,
                    "Closed by the WebSocketTransport",
                )
            except Exception:
                """
                Any exception thrown here will be caused by the socket already being closed,
                which is the state we want to put it in by calling this method, which
                means we don't care if it was already closed and threw an exception
                when we tried to close it again.
                """
                pass

    # TODO: might need to remove offset and count if no segmentation possible
    # TODO: considering to create a BFTransportBuffer class to abstract the logic of binary buffers adapting to
    #  current interfaces
    async def receive(
        self, buffer: List[int], offset: int = None, count: int = None
    ) -> int:
        try:
            if self._socket:
                result = await self._socket.receive()
                buffer_index = buffer.index(None) if None in buffer else 0
                result_index = 0
                while (
                    buffer_index < len(buffer)
                    and result_index < len(result.data)
                    and result_index < count
                ):
                    buffer[buffer_index] = result.data[result_index]
                    buffer_index += 1
                    result_index += 1
                if result.message_type == WebSocketMessageType.CLOSE:
                    await self._socket.close(
                        WebSocketCloseStatus.NORMAL_CLOSURE, "Socket closed"
                    )

                    # Depending on ws implementation library next line might not be necessary
                    if self._socket.status == WebSocketState.CLOSED:
                        self._socket.dispose()

                return len(result.data)
        except Exception as error:
            # Exceptions of the three types below will also have set the socket's state to closed, which fires an
            # event consumers of this class are subscribed to and have handling around. Any other exception needs to
            # be thrown to cause a non-transport-connectivity failure.
            raise error

    # TODO: might need to remove offset and count if no segmentation possible (or put them in BFTransportBuffer)
    async def send(
        self, buffer: List[int], offset: int = None, count: int = None
    ) -> int:
        try:
            if self._socket:
                await self._socket.send(buffer, WebSocketMessageType.BINARY, True)
                return count or len(buffer)
        except Exception as error:
            # Exceptions of the three types below will also have set the socket's state to closed, which fires an
            # event consumers of this class are subscribed to and have handling around. Any other exception needs to
            # be thrown to cause a non-transport-connectivity failure.
            raise error

        return 0
