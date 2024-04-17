# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Optional

from aiohttp import ClientSession
from aiohttp.web import (
    Request,
    Response,
    json_response,
    WebSocketResponse,
    HTTPBadRequest,
    HTTPUnauthorized,
    HTTPUnsupportedMediaType,
)
from botbuilder.core import Bot, BotFrameworkAdapterSettings
from botbuilder.core.streaming import (
    BotFrameworkHttpAdapterBase,
    StreamingRequestHandler,
)
from botbuilder.schema import Activity, ResourceResponse
from botbuilder.integration.aiohttp.streaming import AiohttpWebSocket
from botframework.connector.auth import AuthenticationConstants, JwtTokenValidation


class BotFrameworkHttpAdapter(BotFrameworkHttpAdapterBase):
    def __init__(self, settings: BotFrameworkAdapterSettings):
        # pylint: disable=invalid-name
        super().__init__(settings)

        self._AUTH_HEADER_NAME = "authorization"
        self._CHANNEL_ID_HEADER_NAME = "channelid"

    async def process(
        self, request: Request, ws_response: WebSocketResponse, bot: Bot
    ) -> Optional[Response]:
        # TODO: maybe it's not necessary to expose the ws_response
        if not request:
            raise TypeError("request can't be None")
        # if ws_response is None:
        # raise TypeError("ws_response can't be None")
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

    async def send_streaming_activity(self, activity: Activity) -> ResourceResponse:
        # Check to see if any of this adapter's StreamingRequestHandlers is associated with this conversation.
        possible_handlers = [
            handler
            for handler in self.request_handlers
            if handler.service_url == activity.service_url
            and handler.has_conversation(activity.conversation.id)
        ]

        if possible_handlers:
            if len(possible_handlers) > 1:
                # The conversation has moved to a new connection and the former
                # StreamingRequestHandler needs to be told to forget about it.
                possible_handlers.sort(
                    key=lambda handler: handler.conversation_added_time(
                        activity.conversation.id
                    )
                )
                correct_handler = possible_handlers[-1]
                for handler in possible_handlers:
                    if handler is not correct_handler:
                        handler.forget_conversation(activity.conversation.id)

                return await correct_handler.send_activity(activity)

            return await possible_handlers[0].send_activity(activity)

        if self.connected_bot:
            # This is a proactive message that will need a new streaming connection opened.
            # The ServiceUrl of a streaming connection follows the pattern "url:[ChannelName]:[Protocol]:[Host]".

            uri = activity.service_url.split(":")
            protocol = uri[len(uri) - 2]
            host = uri[len(uri) - 1]
            # TODO: discuss if should abstract this from current package
            # TODO: manage life cycle of sessions (when should we close them)
            session = ClientSession()
            aiohttp_ws = await session.ws_connect(protocol + host + "/api/messages")
            web_socket = AiohttpWebSocket(aiohttp_ws, session)
            handler = StreamingRequestHandler(self.connected_bot, self, web_socket)

            if self.request_handlers is None:
                self.request_handlers = []

            self.request_handlers.append(handler)

            return await handler.send_activity(activity)

        return None

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

            if self.request_handlers is None:
                self.request_handlers = []

            self.request_handlers.append(request_handler)

            await request_handler.listen()
        except Exception as error:
            import traceback  # pylint: disable=import-outside-toplevel

            traceback.print_exc()
            raise Exception(f"Unable to create transport server. Error: {str(error)}")

    async def _http_authenticate_request(self, request: Request) -> bool:
        # pylint: disable=no-member
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

                self._credentials = (
                    self._credentials
                    or await self._BotFrameworkAdapter__get_app_credentials(
                        self.settings.app_id,
                        AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
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
