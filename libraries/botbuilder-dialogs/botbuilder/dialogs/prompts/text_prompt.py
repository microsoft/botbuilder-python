# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict
from botbuilder.core import TurnContext
from botbuilder.schema import ActivityTypes, Activity
from .datetime_resolution import DateTimeResolution
from .prompt import Prompt
from .confirm_prompt import ConfirmPrompt
from .prompt_options import PromptOptions
from .prompt_recognizer_result import PromptRecognizerResult


class TextPrompt(Prompt):
    # TODO: PromptValidator
    def __init__(self, dialog_id: str, validator: object = None):
        super(TextPrompt, self).__init__(dialog_id, validator)

    async def on_prompt(self, turn_context: TurnContext, state: Dict[str, object], options: PromptOptions, is_retry: bool):
        if not turn_context:
            raise TypeError('TextPrompt.on_prompt(): turn_context cannot be None.')
        if not options:
            raise TypeError('TextPrompt.on_prompt(): options cannot be None.')
        
        if is_retry == True and options.retry_prompt != None:
            await turn_context.send_activity(options.retry_prompt)  
        else:
            if options.prompt != None:
                await turn_context.send_activity(options.prompt)


    async def on_recognize(self, turn_context: TurnContext, state: Dict[str, object], options: PromptOptions) -> PromptRecognizerResult:
        if not turn_context:
            raise TypeError('DateTimePrompt.on_recognize(): turn_context cannot be None.')
        
        result = PromptRecognizerResult()
        if turn_context.activity.type == ActivityTypes.message:
            message = turn_context.activity
            if message.text != None:
                result.succeeded = True
                result.value = message.text
        return result
