# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
from typing import Any, Optional, Union

from aiohttp import ClientWebSocketResponse, WSMsgType, ClientSession
from aiohttp.web import WebSocketResponse

from botbuilder.streaming.transport.web_socket import (
    WebSocket,
    WebSocketMessage,
    WebSocketCloseStatus,
    WebSocketMessageType,
    WebSocketState,
)


class AiohttpWebSocket(WebSocket):
    def __init__(
        self,
        aiohttp_ws: Union[WebSocketResponse, ClientWebSocketResponse],
        session: Optional[ClientSession] = None,
    ):
        self._aiohttp_ws = aiohttp_ws
        self._session = session

    def dispose(self):
        if self._session:
            asyncio.create_task(self._session.close())

    async def close(self, close_status: WebSocketCloseStatus, status_description: str):
        await self._aiohttp_ws.close(
            code=int(close_status), message=status_description.encode("utf8")
        )

    async def receive(self) -> WebSocketMessage:
        message = await self._aiohttp_ws.receive()

        return WebSocketMessage(
            message_type=WebSocketMessageType(int(message.type)),
            data=list(str(message.data).encode("utf8"))
            if message.type == WSMsgType.TEXT
            else list(message.data),
        )

    async def send(
        self, buffer: Any, message_type: WebSocketMessageType, end_of_message: bool
    ):
        if message_type == WebSocketMessageType.BINARY:
            await self._aiohttp_ws.send_bytes(buffer)
        elif message_type == WebSocketMessageType.TEXT:
            await self._aiohttp_ws.send_str(buffer)
        else:
            raise RuntimeError(
                f"AiohttpWebSocket - message_type: {message_type} currently not supported"
            )

    @property
    async def status(self) -> WebSocketState:
        return WebSocketState.CLOSED if self._aiohttp_ws.closed else WebSocketState.OPEN
