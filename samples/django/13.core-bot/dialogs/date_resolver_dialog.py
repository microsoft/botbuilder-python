# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext
from botbuilder.dialogs.prompts import DateTimePrompt, PromptValidatorContext, PromptOptions, DateTimeResolution
from .cancel_and_help_dialog import CancelAndHelpDialog
from datatypes_date_time.timex import Timex
class DateResolverDialog(CancelAndHelpDialog):

    def __init__(self, dialog_id: str = None):
        super(DateResolverDialog, self).__init__(dialog_id or DateResolverDialog.__name__)

        self.add_dialog(DateTimePrompt(DateTimePrompt.__name__, DateResolverDialog.datetime_prompt_validator))
        self.add_dialog(WaterfallDialog(WaterfallDialog.__name__ + '2', [
            self.initialStep,
            self.finalStep
        ]))

        self.initial_dialog_id = WaterfallDialog.__name__ + '2'
    
    async def initialStep(self,step_context: WaterfallStepContext) -> DialogTurnResult:
        timex = step_context.options

        prompt_msg = 'On what date would you like to travel?'
        reprompt_msg = "I'm sorry, for best results, please enter your travel date including the month, day and year."

        if timex is None:
            # We were not given any date at all so prompt the user.
            return await step_context.prompt(DateTimePrompt.__name__ ,
                PromptOptions(
                    prompt= MessageFactory.text(prompt_msg),
                    retry_prompt= MessageFactory.text(reprompt_msg)
                ))
        else:
            # We have a Date we just need to check it is unambiguous.
            if 'definite' in Timex(timex).types:
                # This is essentially a "reprompt" of the data we were given up front.
                return await step_context.prompt(DateTimePrompt.__name__, PromptOptions(prompt= reprompt_msg))
            else:
                return await step_context.next(DateTimeResolution(timex= timex))

    async def finalStep(self, step_context: WaterfallStepContext):
        timex = step_context.result[0].timex
        return await step_context.end_dialog(timex)
    
    @staticmethod
    async def datetime_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        if prompt_context.recognized.succeeded:
            timex = prompt_context.recognized.value[0].timex.split('T')[0]

            #TODO: Needs TimexProperty
            return 'definite' in Timex(timex).types
        
        return False
