# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Awaitable, Callable, List

from botbuilder.core import (
    Bot,
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    InvokeResponse,
    TurnContext,
)
from botbuilder.schema import Activity
from botframework.connector.aio import ConnectorClient
from botframework.connector.auth import (
    ClaimsIdentity,
    MicrosoftAppCredentials,
    MicrosoftGovernmentAppCredentials,
)

from .streaming_activity_processor import StreamingActivityProcessor
from .streaming_request_handler import StreamingRequestHandler


class BotFrameworkHttpAdapterBase(BotFrameworkAdapter, StreamingActivityProcessor):
    def __init__(self, settings: BotFrameworkAdapterSettings):
        super().__init__(self, settings)

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

        connector_client = self.create_connector_client()

    def _create_streaming_connector_client(
        self, activity: Activity, request_handler: StreamingRequestHandler
    ) -> ConnectorClient:
        empty_credentials = (
            MicrosoftAppCredentials.empty()
            if self._channel_provider and self._channel_provider.is_government()
            else MicrosoftGovernmentAppCredentials.empty()
        )

        streaming_client
