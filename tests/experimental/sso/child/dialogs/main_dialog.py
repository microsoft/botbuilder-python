# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    DialogTurnResult,
    OAuthPrompt,
    OAuthPromptSettings,
    WaterfallDialog,
    WaterfallStepContext
)
from botbuilder.schema import TokenResponse
from botbuilder.core import MessageFactory
from botframework.connector.auth import MicrosoftAppCredentials

from config import DefaultConfig


class MainDialog(ComponentDialog):
    def __init__(self, config: DefaultConfig):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self.connection_name = config.CONNECTION_NAME
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [self.sign_in_step, self.show_token_response]
            )
        )
        self.add_dialog(
            OAuthPrompt(
                OAuthPrompt.__name__,
                OAuthPromptSettings(
                    connection_name=self.connection_name,
                    text="Sign In to AAD",
                    title="Sign In",
                    oauth_app_credentials=MicrosoftAppCredentials(
                        app_id=config.APP_ID,
                        password=config.APP_PASSWORD
                    )
                )
            )
        )

    async def sign_in_step(self, context: WaterfallStepContext) -> DialogTurnResult:
        return await context.begin_dialog(OAuthPrompt.__name__)

    async def show_token_response(self, context: WaterfallStepContext) -> DialogTurnResult:
        result: TokenResponse = context.result
        if not result:
            await context.context.send_activity(MessageFactory.text("Skill: No token response from OAuthPrompt"))
        else:
            await context.context.send_activity(MessageFactory.text(f"Skill: Your token is {result.token}"))

        return await context.end_dialog()
