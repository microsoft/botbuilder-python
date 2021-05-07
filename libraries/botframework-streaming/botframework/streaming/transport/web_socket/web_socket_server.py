# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from asyncio import Future, iscoroutinefunction, isfuture
from typing import Callable

from botframework.streaming import (
    ProtocolAdapter,
    ReceiveResponse,
    RequestHandler,
    StreamingRequest,
)
from botframework.streaming.payloads import RequestManager
from botframework.streaming.payload_transport import PayloadSender, PayloadReceiver
from botframework.streaming.transport import DisconnectedEventArgs

from .web_socket import WebSocket
from .web_socket_transport import WebSocketTransport


class WebSocketServer:
    def __init__(self, socket: WebSocket, request_handler: RequestHandler):
        if socket is None:
            raise TypeError(
                f"'socket: {socket.__class__.__name__}' argument can't be None"
            )
        if not request_handler:
            raise TypeError(
                f"'request_handler: {request_handler.__class__.__name__}' argument can't be None"
            )

        self.disconnected_event_handler: Callable[
            [object, DisconnectedEventArgs], None
        ] = None

        self._web_socket_transport = WebSocketTransport(socket)
        self._request_handler = request_handler
        self._request_manager = RequestManager()
        self._sender = PayloadSender()
        self._sender.disconnected = self._on_connection_disconnected
        self._receiver = PayloadReceiver()
        self._receiver.disconnected = self._on_connection_disconnected
        self._protocol_adapter = ProtocolAdapter(
            self._request_handler, self._request_manager, self._sender, self._receiver
        )
        self._closed_signal: Future = None
        self._is_disconnecting: bool = False

    @property
    def is_connected(self) -> bool:
        return self._sender.is_connected and self._receiver.is_connected

    async def start(self):
        self._closed_signal = Future()
        self._sender.connect(self._web_socket_transport)
        await self._receiver.connect(self._web_socket_transport)

        return self._closed_signal

    async def send(self, request: StreamingRequest) -> ReceiveResponse:
        if not request:
            raise TypeError(
                f"'request: {request.__class__.__name__}' argument can't be None"
            )

        if not self._sender.is_connected or not self._sender.is_connected:
            raise RuntimeError("The server is not connected")

        return await self._protocol_adapter.send_request(request)

    async def disconnect(self):
        await self._sender.disconnect()
        await self._receiver.disconnect()

    async def _on_connection_disconnected(
        self, sender: object, event_args: object  # pylint: disable=unused-argument
    ):
        if not self._is_disconnecting:
            self._is_disconnecting = True

            if self._closed_signal:
                self._closed_signal.set_result("close")
                self._closed_signal = None

            if sender in [self._sender, self._receiver]:
                if iscoroutinefunction(sender.disconnect) or isfuture(
                    sender.disconnect
                ):
                    await sender.disconnect()
                else:
                    sender.disconnect()

            if self.disconnected_event_handler:
                # pylint: disable=not-callable
                self.disconnected_event_handler(self, DisconnectedEventArgs.empty)

            self._is_disconnecting = False
