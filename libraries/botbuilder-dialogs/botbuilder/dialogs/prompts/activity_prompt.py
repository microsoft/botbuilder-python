# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from typing import Dict

from botbuilder.core import TurnContext
from botbuilder.dialogs import Dialog, DialogContext, DialogInstance, DialogReason
from botbuilder.schema import Activity, InputHints

from .prompt_options import PromptOptions
from .prompt_recognizer_result import PromptRecognizerResult
from .prompt_validator_context import PromptValidatorContext


class ActivityPrompt(Dialog, ABC):
# class ActivityPrompt(ABC):
    """
    Waits for an activity to be received.

    This prompt requires a validator be passed in and is useful when waiting for non-message
    activities like an event to be received. The validator can ignore received events until the
    expected activity is received.
    """
    persisted_options = "options"
    persisted_state = "state"
    # !!! build out PromptValidator class to give type to validator parameter here
    def __init__(self, dialog_id: str, validator ):
        """
        Initializes a new instance of the ActivityPrompt class.

        Parameters:

        dialog_id (str): Unique ID of the dialog within its parent DialogSet or ComponentDialog.

        validator (PromptValidator): Validator that will be called each time a new activity is received.
        """
        self._validator = validator

        persisted_options: str = 'options'
        persisted_state: str = 'state'
    
    async def begin_dialog(self, dc: DialogContext, opt: PromptOptions):
        # Ensure prompts have input hint set
        opt: PromptOptions = PromptOptions(**opt)
        if opt and hasattr(opt, 'prompt') and not hasattr(opt.prompt, 'input_hint'):
            opt.prompt.input_hint = InputHints.expecting_input

        if opt and hasattr(opt, 'retry_prompt') and not hasattr(opt.retry_prompt, 'input_hint'):
            opt.prompt.retry_prompt = InputHints.expecting_input

        # Initialize prompt state
        state: Dict[str, object] = dc.active_dialog.state
        state[self.persisted_options] = opt
        state[self.persisted_state] = {}

        # Send initial prompt
        await self.on_prompt(
            dc.context, 
            state[self.persisted_state], 
            state[self.persisted_options]
        )

        return Dialog.end_of_turn

    async def continue_dialog(self, dc: DialogContext):
        # Perform base recognition
        instance = dc.active_dialog
        state: Dict[str, object] = instance.state[self.persisted_state]
        options: Dict[str, object] = instance.state[self.persisted_options]

        recognized: PromptRecognizerResult = await self.on_recognize(dc.context, state, options)

        # Validate the return value
        prompt_context = PromptValidatorContext(
            dc.context,
            recognized,
            state,
            options
        )

        is_valid = await self._validator(prompt_context)

        # Return recognized value or re-prompt
        if is_valid:
            return await dc.end_dialog(recognized.value)
        else:
            return Dialog.end_of_turn

    async def resume_dialog(self, dc: DialogContext, reason: DialogReason, result: object = None):
        """
        Prompts are typically leaf nodes on the stack but the dev is free to push other dialogs
        on top of the stack which will result in the prompt receiving an unexpected call to
        resume_dialog() when the pushed on dialog ends.
        To avoid the prompt prematurely ending, we need to implement this method and
        simply re-prompt the user
        """
        await self.reprompt_dialog(dc.context, dc.active_dialog)

        return Dialog.end_of_turn
    
    async def reprompt_dialog(self, context: TurnContext, instance: DialogInstance):
        state: Dict[str, object] = instance.state[self.persisted_state]
        options: PromptOptions = instance.state[self.persisted_options]
        await self.on_prompt(context, state, options, True)

    async def on_prompt(
        self, 
        context: TurnContext, 
        state: Dict[str, dict], 
        options: PromptOptions,
        isRetry: bool = False
    ):
        if isRetry and options.retry_prompt:
            options.retry_prompt.input_hint = InputHints.expecting_input
            await context.send_activity(options.retry_prompt)
        elif options.prompt:
            options.prompt = InputHints.expecting_input
            await context.send_activity(options.prompt)
    
    async def on_recognize(
        self, 
        context: TurnContext,
        state: Dict[str, object],
        options: PromptOptions
    ) -> PromptRecognizerResult:

        result = PromptRecognizerResult()
        result.succeeded = True,
        result.value = context.activity

        return result