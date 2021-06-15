# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC
from typing import List, Any

from .web_socket_close_status import WebSocketCloseStatus
from .web_socket_state import WebSocketState
from .web_socket_message_type import WebSocketMessageType


class WebSocketMessage:
    def __init__(self, *, message_type: WebSocketMessageType, data: List[int]):
        self.message_type = message_type
        self.data = data


class WebSocket(ABC):
    def dispose(self):
        raise NotImplementedError()

    async def close(self, close_status: WebSocketCloseStatus, status_description: str):
        raise NotImplementedError()

    async def receive(self) -> WebSocketMessage:
        raise NotImplementedError()

    async def send(
        self, buffer: Any, message_type: WebSocketMessageType, end_of_message: bool
    ):
        raise NotImplementedError()

    @property
    def status(self) -> WebSocketState:
        raise NotImplementedError()
