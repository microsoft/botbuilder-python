# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import sys
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    ConversationState,
    MessageFactory,
    TurnContext,
)
from botbuilder.schema import InputHints


class AdapterWithErrorHandler(BotFrameworkAdapter):
    def __init__(
        self,
        settings: BotFrameworkAdapterSettings,
        conversation_state: ConversationState,
    ):
        super().__init__(settings)
        self._conversation_state = conversation_state

        # Catch-all for errors.
        async def on_error(context: TurnContext, error: Exception):
            # This check writes out errors to console log
            # NOTE: In production environment, you should consider logging this to Azure
            #       application insights.
            print(f"\n [on_turn_error]: {error}", file=sys.stderr)

            # Send a message to the user
            error_message_text = "Sorry, it looks like something went wrong."
            error_message = MessageFactory.text(
                error_message_text, error_message_text, InputHints.expecting_input
            )
            await context.send_activity(error_message)
            # Clear out state
            nonlocal self
            await self._conversation_state.delete(context)

        self.on_turn_error = on_error
