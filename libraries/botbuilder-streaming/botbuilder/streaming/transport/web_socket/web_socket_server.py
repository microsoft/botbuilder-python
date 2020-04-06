# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.streaming import RequestHandler
from botbuilder.streaming.payloads import RequestManager
from botbuilder.streaming.payload_transport import PayloadSender, PayloadReceiver

from .web_socket import WebSocket
from .web_socket_transport import WebSocketTransport


class WebSocketServer:
    def __init__(self, socket: WebSocket, request_handler: RequestHandler):
        if not socket:
            raise TypeError(
                f"'socket: {socket.__class__.__name__}' argument can't be None"
            )
        if not request_handler:
            raise TypeError(
                f"'request_handler: {request_handler.__class__.__name__}' argument can't be None"
            )

        self._web_socket_transport = WebSocketTransport(socket)
        self._request_handler = request_handler
        self._request_manager = RequestManager()
        self._sender = PayloadSender()
        self._sender.disconnected = self._on_connection_disconnected
        self._receiver = PayloadReceiver()
        self._receiver.disconnected = self._on_connection_disconnected
