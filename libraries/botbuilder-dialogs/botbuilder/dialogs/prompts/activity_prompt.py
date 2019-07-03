# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from typing import Callable, Dict

from botbuilder.core import TurnContext
from botbuilder.dialogs import Dialog, DialogContext, DialogInstance, DialogReason, DialogTurnResult
from botbuilder.schema import Activity, ActivityTypes, InputHints

from .prompt import Prompt
from .prompt_options import PromptOptions
from .prompt_recognizer_result import PromptRecognizerResult
from .prompt_validator_context import PromptValidatorContext


class ActivityPrompt(Dialog, ABC):
    """
    Waits for an activity to be received.

    This prompt requires a validator be passed in and is useful when waiting for non-message
    activities like an event to be received. The validator can ignore received events until the
    expected activity is received.
    """
    persisted_options = "options"
    persisted_state = "state"

    def __init__(self, dialog_id: str, validator: Callable[[PromptValidatorContext], bool]):
        """
        Initializes a new instance of the ActivityPrompt class.

        Parameters:
        ----------
        dialog_id (str): Unique ID of the dialog within its parent DialogSet or ComponentDialog.

        validator: Validator that will be called each time a new activity is received.
        """
        Dialog.__init__(self, dialog_id)
        
        if validator is None:
            raise TypeError('validator was expected but received None')
        self._validator = validator

    async def begin_dialog(self, dc: DialogContext, options: PromptOptions) -> DialogTurnResult:
        if not dc:
            raise TypeError('ActivityPrompt.begin_dialog(): dc cannot be None.')
        if not isinstance(options, PromptOptions):
            raise TypeError('ActivityPrompt.begin_dialog(): Prompt options are required for ActivityPrompts.')
        
        # Ensure prompts have input hint set
        if options.prompt is not None and not options.prompt.input_hint:
            options.prompt.input_hint = InputHints.expecting_input

        if options.retry_prompt is not None and not options.retry_prompt.input_hint:
            options.retry_prompt.input_hint = InputHints.expecting_input

        # Initialize prompt state
        state: Dict[str, object] = dc.active_dialog.state
        state[self.persisted_options] = options
        state[self.persisted_state] = {
            Prompt.ATTEMPT_COUNT_KEY: 0
        }

        # Send initial prompt
        await self.on_prompt(
            dc.context, 
            state[self.persisted_state], 
            state[self.persisted_options],
            False
        )

        return Dialog.end_of_turn

    async def continue_dialog(self, dc: DialogContext) -> DialogTurnResult:
        if not dc:
            raise TypeError('ActivityPrompt.continue_dialog(): DialogContext cannot be None.')
            
        # Perform base recognition
        instance = dc.active_dialog
        state: Dict[str, object] = instance.state[self.persisted_state]
        options: Dict[str, object] = instance.state[self.persisted_options]
        recognized: PromptRecognizerResult = await self.on_recognize(dc.context, state, options)

        # Increment attempt count
        state[Prompt.ATTEMPT_COUNT_KEY] += 1

        # Validate the return value
        is_valid = False
        if self._validator is not None:
            prompt_context = PromptValidatorContext(
                dc.context,
                recognized,
                state,
                options
            )
            is_valid = await self._validator(prompt_context)

            if options is None:
                options = PromptOptions()

            options.number_of_attempts += 1
        elif recognized.succeeded:
                is_valid = True
            
        # Return recognized value or re-prompt
        if is_valid:
            return await dc.end_dialog(recognized.value)
        else:
            if dc.context.activity.type == ActivityTypes.message and not dc.context.responded:
                await self.on_prompt(dc.context, state, options, True)

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
        await self.on_prompt(context, state, options, False)

    async def on_prompt(
        self, 
        context: TurnContext, 
        state: Dict[str, dict], 
        options: PromptOptions,
        is_retry: bool = False
    ):
        """
        Called anytime the derived class should send the user a prompt.

        Parameters:
        ----------
        context: Context for the current turn of conversation with the user.

        state: Additional state being persisted for the prompt.

        options: Options that the prompt started with in the call to `DialogContext.prompt()`.

        isRetry: If `true` the users response wasn't recognized and the re-prompt should be sent.
        """
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

        result = PromptRecognizerResult()
        result.succeeded = True,
        result.value = context.activity

        return result