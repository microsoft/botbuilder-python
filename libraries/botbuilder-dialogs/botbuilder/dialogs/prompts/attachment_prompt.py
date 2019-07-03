# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Callable, Dict, List

from botbuilder.schema import ActivityTypes, Attachment, InputHints
from botbuilder.core import TurnContext

from .prompt import Prompt
from .prompt_options import PromptOptions
from .prompt_recognizer_result import PromptRecognizerResult
from .prompt_validator_context import PromptValidatorContext

class AttachmentPrompt(Prompt):
    """
    Prompts a user to upload attachments like images.

    By default the prompt will return to the calling dialog an `[Attachment]`
    """

    def __init__(self, dialog_id: str, validator: Callable[[Attachment], bool] = None):
        super().__init__(dialog_id, validator)
    
    async def on_prompt(
        self,
        context: TurnContext,
        state: Dict[str, object],
        options: PromptOptions,
        is_retry: bool
    ):
        if not context:
            raise TypeError('AttachmentPrompt.on_prompt(): TurnContext cannot be None.')

        if not isinstance(options, PromptOptions):
            raise TypeError('AttachmentPrompt.on_prompt(): PromptOptions are required for Attachment Prompt dialogs.')
        
        if is_retry and options.retry_prompt:
            options.retry_prompt.input_hint = InputHints.expecting_input
            await context.send_activity(options.retry_prompt)
        elif options.prompt:
            options.prompt.input_hint = InputHints.expecting_input
            await context.send_activity(options.prompt)
    
    async def on_recognize(
        self,
        context: TurnContext,
        state: Dict[str, object],
        options: PromptOptions
    ) -> PromptRecognizerResult:
        if not context:
            raise TypeError('AttachmentPrompt.on_recognize(): context cannot be None.')
        
        result = PromptRecognizerResult()

        if context.activity.type == ActivityTypes.message:
            message = context.activity
            if isinstance(message.attachments, list) and len(message.attachments) > 0:
                result.succeeded = True
                result.value = message.attachments
        
        return result
