# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import ConfirmPrompt, PromptOptions, OAuthPrompt, OAuthPromptSettings
from botbuilder.core import MessageFactory
from dialogs import LogoutDialog


class MainDialog(LogoutDialog):
    def __init__(
        self, configuration,
    ):
        super().__init__(MainDialog.__name__, configuration.CONNECTION_NAME)

        self.add_dialog(
            OAuthPrompt(
                OAuthPrompt.__name__,
                OAuthPromptSettings(
                    connection_name=self.connection_name,
                    text="Please Sign In",
                    title="Sign In",
                    timeout=30000,
                )
            )
        )
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [self.prompt_step, self.login_step, self.display_token_phase_one, self.display_token_phase_two]
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def prompt_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.begin_dialog(
            OAuthPrompt.__name__
        )

    async def login_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        token_response = step_context.result
        if token_response:
            await step_context.context.send_activity(MessageFactory.text("You are now logged in."))
            return await step_context.prompt(
                ConfirmPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Would you like to view your token?"))
            )

        await step_context.context.send_activity(MessageFactory.text("Login was not successful please try again."))
        return await step_context.end_dialog()

    async def display_token_phase_one(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        await step_context.context.send_activity(MessageFactory.text("Thank you"))

        result = step_context.result
        if result:
            return await step_context.begin_dialog(OAuthPrompt.__name__)

        return await step_context.end_dialog()

    async def display_token_phase_two(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        token_response = step_context.result
        if token_response:
            await step_context.context.send_activity(MessageFactory.text(f"Here is your token {token_response.token}"))

        return await step_context.end_dialog()
