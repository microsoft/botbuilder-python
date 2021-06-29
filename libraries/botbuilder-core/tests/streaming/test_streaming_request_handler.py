# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from unittest.mock import Mock
from typing import Any

import aiounittest

from botbuilder.core.streaming import StreamingRequestHandler
from botframework.streaming.transport.web_socket import (
    WebSocket,
    WebSocketState,
    WebSocketCloseStatus,
    WebSocketMessage,
    WebSocketMessageType,
)


class MockWebSocket(WebSocket):
    # pylint: disable=unused-argument
    def __init__(self):
        super(MockWebSocket, self).__init__()

        self.receive_called = False

    def dispose(self):
        return

    async def close(self, close_status: WebSocketCloseStatus, status_description: str):
        return

    async def receive(self) -> WebSocketMessage:
        self.receive_called = True

    async def send(
        self, buffer: Any, message_type: WebSocketMessageType, end_of_message: bool
    ):
        raise Exception

    @property
    def status(self) -> WebSocketState:
        return WebSocketState.OPEN


class TestStramingRequestHandler(aiounittest.AsyncTestCase):
    async def test_listen(self):
        mock_bot = Mock()
        mock_activity_processor = Mock()
        mock_web_socket = MockWebSocket()

        sut = StreamingRequestHandler(
            mock_bot, mock_activity_processor, mock_web_socket
        )
        await sut.listen()

        assert mock_web_socket.receive_called
