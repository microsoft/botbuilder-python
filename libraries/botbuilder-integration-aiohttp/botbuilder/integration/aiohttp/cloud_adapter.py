# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Awaitable, Callable, Optional

from aiohttp.web import (
    Request,
    Response,
    json_response,
    WebSocketResponse,
    HTTPBadRequest,
    HTTPMethodNotAllowed,
    HTTPUnauthorized,
    HTTPUnsupportedMediaType,
)
from botbuilder.core import (
    Bot,
    CloudAdapterBase,
    InvokeResponse,
    TurnContext,
)
from botbuilder.core.streaming import (
    StreamingActivityProcessor,
    StreamingHttpDriver,
    StreamingRequestHandler,
)
from botbuilder.schema import Activity
from botbuilder.integration.aiohttp.streaming import AiohttpWebSocket
from botframework.connector import AsyncBfPipeline, BotFrameworkConnectorConfiguration
from botframework.connector.aio import ConnectorClient
from botframework.connector.auth import (
    AuthenticateRequestResult,
    BotFrameworkAuthentication,
    BotFrameworkAuthenticationFactory,
    ConnectorFactory,
    MicrosoftAppCredentials,
)

from .bot_framework_http_adapter_integration_base import (
    BotFrameworkHttpAdapterIntegrationBase,
)


class CloudAdapter(CloudAdapterBase, BotFrameworkHttpAdapterIntegrationBase):
    def __init__(self, bot_framework_authentication: BotFrameworkAuthentication = None):
        """
        Initializes a new instance of the CloudAdapter class.

        :param bot_framework_authentication: Optional BotFrameworkAuthentication instance
        """
        # pylint: disable=invalid-name
        if not bot_framework_authentication:
            bot_framework_authentication = BotFrameworkAuthenticationFactory.create()

        self._AUTH_HEADER_NAME = "authorization"
        self._CHANNEL_ID_HEADER_NAME = "channelid"
        super().__init__(bot_framework_authentication)

    async def process(
        self, request: Request, bot: Bot, ws_response: WebSocketResponse = None
    ) -> Optional[Response]:
        if not request:
            raise TypeError("request can't be None")
        # if ws_response is None:
        # raise TypeError("ws_response can't be None")
        if not bot:
            raise TypeError("bot can't be None")
        try:
            # Only GET requests for web socket connects are allowed
            if (
                request.method == "GET"
                and ws_response
                and ws_response.can_prepare(request)
            ):
                # All socket communication will be handled by the internal streaming-specific BotAdapter
                await self._connect(bot, request, ws_response)
            elif request.method == "POST":
                # Deserialize the incoming Activity
                if "application/json" in request.headers["Content-Type"]:
                    body = await request.json()
                else:
                    raise HTTPUnsupportedMediaType()

                activity: Activity = Activity().deserialize(body)

                # A POST request must contain an Activity
                if not activity.type:
                    raise HTTPBadRequest

                # Grab the auth header from the inbound http request
                auth_header = (
                    request.headers["Authorization"]
                    if "Authorization" in request.headers
                    else ""
                )

                # Process the inbound activity with the bot
                invoke_response = await self.process_activity(
                    auth_header, activity, bot.on_turn
                )

                # Write the response, serializing the InvokeResponse
                if invoke_response:
                    return json_response(
                        data=invoke_response.body, status=invoke_response.status
                    )
                return Response(status=201)
            else:
                raise HTTPMethodNotAllowed
        except (HTTPUnauthorized, PermissionError) as _:
            raise HTTPUnauthorized

    async def _connect(
        self, bot: Bot, request: Request, ws_response: WebSocketResponse
    ):
        if ws_response is None:
            raise TypeError("ws_response can't be None")

        # Grab the auth header from the inbound http request
        auth_header = request.headers.get(self._AUTH_HEADER_NAME)
        # Grab the channelId which should be in the http headers
        channel_id = request.headers.get(self._CHANNEL_ID_HEADER_NAME)

        authentication_request_result = (
            await self.bot_framework_authentication.authenticate_streaming_request(
                auth_header, channel_id
            )
        )

        # Transition the request to a WebSocket connection
        await ws_response.prepare(request)
        bf_web_socket = AiohttpWebSocket(ws_response)

        streaming_activity_processor = _StreamingActivityProcessor(
            authentication_request_result, self, bot, bf_web_socket
        )

        await streaming_activity_processor.listen()


class _StreamingActivityProcessor(StreamingActivityProcessor):
    def __init__(
        self,
        authenticate_request_result: AuthenticateRequestResult,
        adapter: CloudAdapter,
        bot: Bot,
        web_socket: AiohttpWebSocket = None,
    ) -> None:
        self._authenticate_request_result = authenticate_request_result
        self._adapter = adapter

        # Internal reuse of the existing StreamingRequestHandler class
        self._request_handler = StreamingRequestHandler(bot, self, web_socket)

        # Fix up the connector factory so connector create from it will send over this connection
        self._authenticate_request_result.connector_factory = (
            _StreamingConnectorFactory(self._request_handler)
        )

    async def listen(self):
        await self._request_handler.listen()

    async def process_streaming_activity(
        self,
        activity: Activity,
        bot_callback_handler: Callable[[TurnContext], Awaitable],
    ) -> InvokeResponse:
        return await self._adapter.process_activity(
            self._authenticate_request_result, activity, bot_callback_handler
        )


class _StreamingConnectorFactory(ConnectorFactory):
    def __init__(self, request_handler: StreamingRequestHandler) -> None:
        self._request_handler = request_handler
        self._service_url = None

    async def create(
        self, service_url: str, audience: str  # pylint: disable=unused-argument
    ) -> ConnectorClient:
        if not self._service_url:
            self._service_url = service_url
        elif service_url != self._service_url:
            raise RuntimeError(
                "This is a streaming scenario, all connectors from this factory must all be for the same url."
            )

        # TODO: investigate if Driver and pipeline should be moved here
        streaming_driver = StreamingHttpDriver(self._request_handler)
        config = BotFrameworkConnectorConfiguration(
            MicrosoftAppCredentials.empty(),
            service_url,
            pipeline_type=AsyncBfPipeline,
            driver=streaming_driver,
        )
        streaming_driver.config = config
        connector_client = ConnectorClient(None, custom_configuration=config)

        return connector_client
