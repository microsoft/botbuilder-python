# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    MessageFactory,
    TurnContext
)


class AdapterWithErrorHandler(BotFrameworkAdapter):
    def __init__(
        self,
        settings: BotFrameworkAdapterSettings
    ):
        super().__init__(settings)

        # Catch-all for errors.
        async def on_error(context: TurnContext, error: Exception):
            # This check writes out errors to console log
            # NOTE: In production environment, you should consider logging this to Azure
            #       application insights.
            print(f"\n [on_turn_error]: {error}", file=sys.stderr)

            # Send a message to the user
            error_message_text = "Sorry, it looks like something went wrong."
            await context.send_activity(MessageFactory.text(error_message_text))

        self.on_turn_error = on_error
