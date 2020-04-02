# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.streaming import RequestHandler

from .web_socket import WebSocket


class WebSocketServer:
    def __init__(self, socket: WebSocket, request_handler: RequestHandler):
        self._request_handler = request_handler
