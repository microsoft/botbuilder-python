# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from http import HTTPStatus
from typing import Awaitable, Callable, List

from aiohttp import ClientSession
from botbuilder.core import (
    Bot,
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    InvokeResponse,
    TurnContext,
)
from botbuilder.schema import Activity, ActivityTypes, ResourceResponse
from botframework.connector import AsyncBfPipeline
from botframework.connector.aio import ConnectorClient
from botframework.connector.auth import (
    ClaimsIdentity,
    MicrosoftAppCredentials,
    MicrosoftGovernmentAppCredentials,
)

from .streaming_activity_processor import StreamingActivityProcessor
from .streaming_request_handler import StreamingRequestHandler
from .streaming_http_client import StreamingHttpDriver
from .aiohttp_web_socket import AiohttpWebSocket


class BotFrameworkHttpAdapterBase(BotFrameworkAdapter, StreamingActivityProcessor):
    def __init__(self, settings: BotFrameworkAdapterSettings):
        super().__init__(settings)

        self.connected_bot: Bot = None
        self.claims_identity: ClaimsIdentity = None
        self.request_handlers: List[StreamingRequestHandler] = None

    async def process_streaming_activity(
        self,
        activity: Activity,
        bot_callback_handler: Callable[[TurnContext], Awaitable],
    ) -> InvokeResponse:
        if not activity:
            raise TypeError(
                f"'activity: {activity.__class__.__name__}' argument can't be None"
            )

        """
        If a conversation has moved from one connection to another for the same Channel or Skill and
        hasn't been forgotten by the previous StreamingRequestHandler. The last requestHandler
        the conversation has been associated with should always be the active connection.
        """
        request_handler = [
            handler
            for handler in self.request_handlers
            if handler.service_url == activity.service_url
            and handler.has_conversation(activity.conversation.id)
        ]
        request_handler = request_handler[-1] if request_handler else None
        context = TurnContext(self, activity)

        if self.claims_identity:
            context.turn_state[self.BOT_IDENTITY_KEY] = self.claims_identity

        connector_client = self._create_streaming_connector_client(
            activity, request_handler
        )
        context.turn_state[self.BOT_CONNECTOR_CLIENT_KEY] = connector_client

        await self.run_pipeline(context, bot_callback_handler)

        if activity.type == ActivityTypes.invoke:
            activity_invoke_response = context.turn_state.get(self._INVOKE_RESPONSE_KEY)

            if not activity_invoke_response:
                return InvokeResponse(status=HTTPStatus.NOT_IMPLEMENTED)
            return activity_invoke_response.value

        return None

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
        else:
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

    def can_process_outgoing_activity(self, activity: Activity) -> bool:
        if not activity:
            raise TypeError(
                f"'activity: {activity.__class__.__name__}' argument can't be None"
            )

        return not activity.service_url.startswith("https")

    async def process_outgoing_activity(
        self, turn_context: TurnContext, activity: Activity
    ) -> ResourceResponse:
        if not activity:
            raise TypeError(
                f"'activity: {activity.__class__.__name__}' argument can't be None"
            )

        # TODO: Check if we have token responses from OAuth cards.

        # The ServiceUrl for streaming channels begins with the string "urn" and contains
        # information unique to streaming connections. Now that we know that this is a streaming
        # activity, process it in the streaming pipeline.
        # Process streaming activity.
        return await self.send_streaming_activity(activity)

    def _create_streaming_connector_client(
        self, activity: Activity, request_handler: StreamingRequestHandler
    ) -> ConnectorClient:
        empty_credentials = (
            MicrosoftAppCredentials.empty()
            if self._channel_provider and self._channel_provider.is_government()
            else MicrosoftGovernmentAppCredentials.empty()
        )

        streaming_driver = StreamingHttpDriver(request_handler)
        connector_client = ConnectorClient(
            empty_credentials,
            activity.service_url,
            pipeline_type=AsyncBfPipeline,
            driver=streaming_driver,
        )

        return connector_client
