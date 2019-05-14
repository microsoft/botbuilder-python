# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict
from botbuilder.core.turn_context import TurnContext
from botbuilder.schema import (ActivityTypes, Activity)
from .prompt import Prompt
from .prompt_options import PromptOptions
from .prompt_recognizer_result import PromptRecognizerResult
from recognizers_number import recognize_number

class NumberPrompt(Prompt):
    # TODO: PromptValidator
    def __init__(self, dialog_id: str, validator: object, default_locale: str):
        super(NumberPrompt, self).__init__(dialog_id, validator)
        self.default_locale = default_locale

    async def on_prompt(self, turn_context: TurnContext, state: Dict[str, object], options: PromptOptions, is_retry: bool):
        if not turn_context:
            raise TypeError('NumberPrompt.on_prompt(): turn_context cannot be None.')
        if not options:
            raise TypeError('NumberPrompt.on_prompt(): options cannot be None.')

        if is_retry == True and options.retry_prompt != None:
            prompt = turn_context.send_activity(options.retry_prompt)
        else:
            if options.prompt != None:
                await turn_context.send_activity(options.prompt)

    async def on_recognize(self, turn_context: TurnContext, state: Dict[str, object], options: PromptOptions) -> PromptRecognizerResult:
        if not turn_context:
            raise TypeError('NumberPrompt.on_recognize(): turn_context cannot be None.')

        result = PromptRecognizerResult()
        if turn_context.activity.type == ActivityTypes.message:
            message = turn_context.activity

            # TODO: Fix constant English with correct constant from text recognizer
            culture = turn_context.activity.locale if turn_context.activity.locale != None else 'English'

            results = recognize_number(message.text, culture)
            if len(results) > 0:
                result.succeeded = True
                result.value = results[0].resolution["value"]

        return result