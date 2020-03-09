# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import MessageFactory
from botbuilder.dialogs import ComponentDialog, DialogTurnResult, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.schema import InputHints


class TangentDialog(ComponentDialog):
    def __init__(self, dialog_id: str = "TangentDialog"):
        super().__init__(dialog_id)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.step_1,
                    self.step_2
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def step_1(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        prompt_message = MessageFactory.text("Tangent step 1 of 2", InputHints.expecting_input)

        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))

    async def step_2(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        prompt_message = MessageFactory.text("Tangent step 2 of 2", InputHints.expecting_input)

        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))
