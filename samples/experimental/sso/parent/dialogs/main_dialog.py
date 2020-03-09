# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    DialogTurnResult,
    WaterfallDialog,
    WaterfallStepContext
)
from botbuilder.dialogs.prompts import (
    OAuthPrompt,
    OAuthPromptSettings
)
from botbuilder.schema import TokenResponse
from botbuilder.core import MessageFactory

from config import DefaultConfig


class MainDialog(ComponentDialog):
    def __init__(self, configuration: DefaultConfig):
        super().__init__(MainDialog.__name__)

        self._connection_name = configuration.CONNECTION_NAME

        self.add_dialog(
            OAuthPrompt(
                OAuthPrompt.__name__,
                OAuthPromptSettings(
                    connection_name=self._connection_name,
                    text=f"Sign In to AAD",
                    title="Sign In",
                ),
            )
        )

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__, [self._sign_in_step, self._show_token_response]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def _sign_in_step(self, context: WaterfallStepContext) -> DialogTurnResult:
        return await context.begin_dialog(OAuthPrompt.__name__)

    async def _show_token_response(self, context: WaterfallStepContext) -> DialogTurnResult:
        result: TokenResponse = context.result

        if not result:
            await context.context.send_activity(MessageFactory.text("No token response from OAuthPrompt"))
        else:
            await context.context.send_activity(MessageFactory.text(f"Your token is {result.token}"))

        return await context.end_dialog()
