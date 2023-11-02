# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from http import HTTPStatus
from typing import Awaitable, Callable, List

from botbuilder.core import (
    Bot,
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    InvokeResponse,
    TurnContext,
)
from botbuilder.schema import Activity, ActivityTypes, ResourceResponse
from botframework.connector import AsyncBfPipeline, BotFrameworkConnectorConfiguration
from botframework.connector.aio import ConnectorClient
from botframework.connector.auth import (
    ClaimsIdentity,
    MicrosoftAppCredentials,
    MicrosoftGovernmentAppCredentials,
)

from .streaming_activity_processor import StreamingActivityProcessor
from .streaming_request_handler import StreamingRequestHandler
from .streaming_http_client import StreamingHttpDriver


class BotFrameworkHttpAdapterBase(BotFrameworkAdapter, StreamingActivityProcessor):
    # pylint: disable=pointless-string-statement
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
        raise NotImplementedError()

    def can_process_outgoing_activity(self, activity: Activity) -> bool:
        if not activity:
            raise TypeError(
                f"'activity: {activity.__class__.__name__}' argument can't be None"
            )

        return not activity.service_url.startswith("https")

    async def process_outgoing_activity(
        self, _turn_context: TurnContext, activity: Activity
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
        config = BotFrameworkConnectorConfiguration(
            empty_credentials,
            activity.service_url,
            pipeline_type=AsyncBfPipeline,
            driver=streaming_driver,
        )
        streaming_driver.config = config
        connector_client = ConnectorClient(None, custom_configuration=config)

        return connector_client
