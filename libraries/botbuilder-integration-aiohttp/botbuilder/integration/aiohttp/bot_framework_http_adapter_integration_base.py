# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from typing import Optional

from aiohttp.web import (
    Request,
    Response,
    WebSocketResponse,
)

from botbuilder.core import Bot


class BotFrameworkHttpAdapterIntegrationBase(ABC):
    @abstractmethod
    async def process(
        self, request: Request, bot: Bot, ws_response: WebSocketResponse = None
    ) -> Optional[Response]:
        raise NotImplementedError()
