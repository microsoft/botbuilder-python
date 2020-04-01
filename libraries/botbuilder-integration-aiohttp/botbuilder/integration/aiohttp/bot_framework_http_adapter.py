from aiohttp.web import Request, Response, WebSocketResponse
from botbuilder.core import BotFrameworkAdapter, Bot


class BotFrameworkHttpAdapter(BotFrameworkAdapter):
    async def process(self, request: Request, ws_response: WebSocketResponse, bot: Bot):
        if not request:
            raise TypeError("request can't be None")
        if not ws_response:
            raise TypeError("ws_response can't be None")
        if not bot:
            raise TypeError("bot can't be None")

        if request.method == "GET":
            await self.connect_web_socket(bot, request, ws_response)

    async def connect_web_socket(
        self, bot: Bot, request: Request, ws_response: WebSocketResponse
    ):
        if not request:
            raise TypeError("request can't be None")
        if not ws_response:
            raise TypeError("ws_response can't be None")

        if not ws_response.can_prepare(request):
            raise Exception("WS not available")
