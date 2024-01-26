# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
import traceback

from typing import Any, Optional, Union

from aiohttp import ClientWebSocketResponse, WSMsgType, ClientSession
from aiohttp.web import WebSocketResponse

from botframework.streaming.transport.web_socket import (
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
            task = asyncio.create_task(self._session.close())

    async def close(self, close_status: WebSocketCloseStatus, status_description: str):
        await self._aiohttp_ws.close(
            code=int(close_status), message=status_description.encode("utf8")
        )

    async def receive(self) -> WebSocketMessage:
        try:
            message = await self._aiohttp_ws.receive()

            if message.type == WSMsgType.TEXT:
                message_data = list(str(message.data).encode("ascii"))
            elif message.type == WSMsgType.BINARY:
                message_data = list(message.data)
            elif isinstance(message.data, int):
                message_data = []

            # async for message in self._aiohttp_ws:
            return WebSocketMessage(
                message_type=WebSocketMessageType(int(message.type)), data=message_data
            )
        except Exception as error:
            traceback.print_exc()
            raise error

    async def send(
        self, buffer: Any, message_type: WebSocketMessageType, end_of_message: bool
    ):
        is_closing = self._aiohttp_ws.closed
        try:
            if message_type == WebSocketMessageType.BINARY:
                # TODO: The clening buffer line should be removed, just for bypassing bug in POC
                clean_buffer = bytes([byte for byte in buffer if byte is not None])
                await self._aiohttp_ws.send_bytes(clean_buffer)
            elif message_type == WebSocketMessageType.TEXT:
                await self._aiohttp_ws.send_str(buffer)
            else:
                raise RuntimeError(
                    f"AiohttpWebSocket - message_type: {message_type} currently not supported"
                )
        except Exception as error:
            traceback.print_exc()
            raise error

    @property
    def status(self) -> WebSocketState:
        return WebSocketState.CLOSED if self._aiohttp_ws.closed else WebSocketState.OPEN
