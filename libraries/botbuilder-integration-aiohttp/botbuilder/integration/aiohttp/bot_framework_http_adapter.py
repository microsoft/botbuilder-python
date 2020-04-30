# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Optional

from aiohttp.web import (
    Request,
    Response,
    json_response,
    WebSocketResponse,
    HTTPBadRequest,
    HTTPUnauthorized,
    HTTPUnsupportedMediaType,
)
from botbuilder.core import Bot, BotFrameworkAdapterSettings, BotFrameworkAdapter
from botbuilder.core.streaming import (
    AiohttpWebSocket,
    BotFrameworkHttpAdapterBase,
    StreamingRequestHandler,
)
from botbuilder.schema import Activity
from botframework.connector.auth import AuthenticationConstants, JwtTokenValidation


class BotFrameworkHttpAdapter(BotFrameworkHttpAdapterBase):
    def __init__(self, settings: BotFrameworkAdapterSettings):
        super().__init__(settings)

        self._AUTH_HEADER_NAME = "authorization"
        self._CHANNEL_ID_HEADER_NAME = "channelid"

    async def process(
        self, request: Request, ws_response: WebSocketResponse, bot: Bot
    ) -> Optional[Response]:
        # TODO: maybe it's not necessary to expose the ws_response
        if not request:
            raise TypeError("request can't be None")
        #if ws_response is None:
            #raise TypeError("ws_response can't be None")
        if not bot:
            raise TypeError("bot can't be None")

        if request.method == "GET":
            await self._connect_web_socket(bot, request, ws_response)
        else:
            # Deserialize the incoming Activity
            if "application/json" in request.headers["Content-Type"]:
                body = await request.json()
            else:
                raise HTTPUnsupportedMediaType()

            activity = Activity().deserialize(body)
            auth_header = (
                request.headers["Authorization"]
                if "Authorization" in request.headers
                else ""
            )

            # Process the inbound activity with the bot
            invoke_response = await self.process_activity(
                activity, auth_header, bot.on_turn
            )
            if invoke_response:
                return json_response(
                    data=invoke_response.body, status=invoke_response.status
                )
            return Response(status=201)

    async def _connect_web_socket(
        self, bot: Bot, request: Request, ws_response: WebSocketResponse
    ):
        if not request:
            raise TypeError("request can't be None")
        if ws_response is None:
            raise TypeError("ws_response can't be None")

        if not bot:
            raise TypeError(f"'bot: {bot.__class__.__name__}' argument can't be None")

        if not ws_response.can_prepare(request):
            raise HTTPBadRequest(text="Upgrade to WebSocket is required.")

        if not await self._http_authenticate_request(request):
            raise HTTPUnauthorized(text="Request authentication failed.")

        try:
            await ws_response.prepare(request)

            bf_web_socket = AiohttpWebSocket(ws_response)

            request_handler = StreamingRequestHandler(bot, self, bf_web_socket)

            # await request_handler._server._receiver.connect(request_handler._server._web_socket_transport)

            if self.request_handlers is None:
                self.request_handlers = []

            self.request_handlers.append(request_handler)

            await request_handler.listen()
        except Exception as error:
            import traceback
            traceback.print_exc()
            raise Exception(f"Unable to create transport server. Error: {str(error)}")

    async def _http_authenticate_request(self, request: Request) -> bool:
        try:
            if not await self._credential_provider.is_authentication_disabled():
                auth_header = request.headers.get(self._AUTH_HEADER_NAME)
                channel_id = request.headers.get(self._CHANNEL_ID_HEADER_NAME)

                if not auth_header:
                    await self._write_unauthorized_response(self._AUTH_HEADER_NAME)
                    return False
                if not channel_id:
                    await self._write_unauthorized_response(
                        self._CHANNEL_ID_HEADER_NAME
                    )
                    return False

                claims_identity = await JwtTokenValidation.validate_auth_header(
                    auth_header,
                    self._credential_provider,
                    self._channel_provider,
                    channel_id,
                )

                if not claims_identity.is_authenticated:
                    raise HTTPUnauthorized()

                self._credentials = self._credentials or await self._BotFrameworkAdapter__get_app_credentials(
                    self.settings.app_id,
                    AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
                )

                # Add ServiceURL to the cache of trusted sites in order to allow token refreshing.
                self._credentials.trust_service_url(
                    claims_identity.claims.get(
                        AuthenticationConstants.SERVICE_URL_CLAIM
                    )
                )
                self.claims_identity = claims_identity
            return True
        except Exception as error:
            raise error

    async def _write_unauthorized_response(self, header_name: str):
        raise HTTPUnauthorized(
            text=f"Unable to authenticate. Missing header: {header_name}"
        )
