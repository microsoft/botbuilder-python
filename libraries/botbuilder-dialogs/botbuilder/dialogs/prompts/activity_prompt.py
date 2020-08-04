# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Callable, Dict

from botbuilder.core import TurnContext
from botbuilder.dialogs import (
    Dialog,
    DialogContext,
    DialogInstance,
    DialogReason,
    DialogTurnResult,
)
from botbuilder.schema import ActivityTypes, InputHints

from .prompt import Prompt
from .prompt_options import PromptOptions
from .prompt_recognizer_result import PromptRecognizerResult
from .prompt_validator_context import PromptValidatorContext


class ActivityPrompt(Dialog):
    """
    Waits for an activity to be received.

        .. remarks::
            This prompt requires a validator be passed in and is useful when waiting for non-message
            activities like an event to be received. The validator can ignore received events until the
            expected activity is received.

    :var persisted_options:
    :typevar persisted_options: str
    :var persisted_state:
    :vartype persisted_state: str
    """

    persisted_options = "options"
    persisted_state = "state"

    def __init__(
        self, dialog_id: str, validator: Callable[[PromptValidatorContext], bool]
    ):
        """
        Initializes a new instance of the :class:`ActivityPrompt` class.

        :param dialog_id: Unique ID of the dialog within its parent :class:`DialogSet` or :class:`ComponentDialog`.
        :type dialog_id: str
        :param validator: Validator that will be called each time a new activity is received.
        :type validator: :class:`typing.Callable[[:class:`PromptValidatorContext`], bool]`
        """
        Dialog.__init__(self, dialog_id)

        if validator is None:
            raise TypeError("validator was expected but received None")
        self._validator = validator

    async def begin_dialog(
        self, dialog_context: DialogContext, options: PromptOptions = None
    ) -> DialogTurnResult:
        """
        Called when a prompt dialog is pushed onto the dialog stack and is being activated.

        :param dialog_context: The dialog context for the current turn of the conversation.
        :type dialog_context: :class:`DialogContext`
        :param options: Optional, additional information to pass to the prompt being started.
        :type options: :class:`PromptOptions`
        :return Dialog.end_of_turn:
        :rtype Dialog.end_of_turn: :class:`Dialog.DialogTurnResult`
        """
        if not dialog_context:
            raise TypeError("ActivityPrompt.begin_dialog(): dc cannot be None.")
        if not isinstance(options, PromptOptions):
            raise TypeError(
                "ActivityPrompt.begin_dialog(): Prompt options are required for ActivityPrompts."
            )

        # Ensure prompts have input hint set
        if options.prompt is not None and not options.prompt.input_hint:
            options.prompt.input_hint = InputHints.expecting_input

        if options.retry_prompt is not None and not options.retry_prompt.input_hint:
            options.retry_prompt.input_hint = InputHints.expecting_input

        # Initialize prompt state
        state: Dict[str, object] = dialog_context.active_dialog.state
        state[self.persisted_options] = options
        state[self.persisted_state] = {Prompt.ATTEMPT_COUNT_KEY: 0}

        # Send initial prompt
        await self.on_prompt(
            dialog_context.context,
            state[self.persisted_state],
            state[self.persisted_options],
            False,
        )

        return Dialog.end_of_turn

    async def continue_dialog(self, dialog_context: DialogContext) -> DialogTurnResult:
        """
        Called when a prompt dialog is the active dialog and the user replied with a new activity.

        :param dialog_context: The dialog context for the current turn of the conversation.
        :type dialog_context: :class:`DialogContext`
        :return Dialog.end_of_turn:
        :rtype Dialog.end_of_turn: :class:`Dialog.DialogTurnResult`
        """
        if not dialog_context:
            raise TypeError(
                "ActivityPrompt.continue_dialog(): DialogContext cannot be None."
            )

        # Perform base recognition
        instance = dialog_context.active_dialog
        state: Dict[str, object] = instance.state[self.persisted_state]
        options: Dict[str, object] = instance.state[self.persisted_options]
        recognized: PromptRecognizerResult = await self.on_recognize(
            dialog_context.context, state, options
        )

        # Increment attempt count
        state[Prompt.ATTEMPT_COUNT_KEY] += 1

        # Validate the return value
        is_valid = False
        if self._validator is not None:
            prompt_context = PromptValidatorContext(
                dialog_context.context, recognized, state, options
            )
            is_valid = await self._validator(prompt_context)

            if options is None:
                options = PromptOptions()

            options.number_of_attempts += 1
        elif recognized.succeeded:
            is_valid = True

        # Return recognized value or re-prompt
        if is_valid:
            return await dialog_context.end_dialog(recognized.value)

        if (
            dialog_context.context.activity.type == ActivityTypes.message
            and not dialog_context.context.responded
        ):
            await self.on_prompt(dialog_context.context, state, options, True)

        return Dialog.end_of_turn

    async def resume_dialog(  # pylint: disable=unused-argument
        self, dialog_context: DialogContext, reason: DialogReason, result: object = None
    ):
        """
        Called when a prompt dialog resumes being the active dialog on the dialog stack, such
        as when the previous active dialog on the stack completes.

        .. remarks::
            Prompts are typically leaf nodes on the stack but the dev is free to push other dialogs
            on top of the stack which will result in the prompt receiving an unexpected call to
            :meth:`ActivityPrompt.resume_dialog()` when the pushed on dialog ends.
            To avoid the prompt prematurely ending, we need to implement this method and
            simply re-prompt the user.

        :param dialog_context: The dialog context for the current turn of the conversation
        :type dialog_context: :class:`DialogContext`
        :param reason: An enum indicating why the dialog resumed.
        :type reason: :class:`DialogReason`
        :param result: Optional, value returned from the previous dialog on the stack.
        :type result: object
        """
        await self.reprompt_dialog(dialog_context.context, dialog_context.active_dialog)

        return Dialog.end_of_turn

    async def reprompt_dialog(self, context: TurnContext, instance: DialogInstance):
        state: Dict[str, object] = instance.state[self.persisted_state]
        options: PromptOptions = instance.state[self.persisted_options]
        await self.on_prompt(context, state, options, False)

    async def on_prompt(
        self,
        context: TurnContext,
        state: Dict[str, dict],  # pylint: disable=unused-argument
        options: PromptOptions,
        is_retry: bool = False,
    ):
        """
        Called anytime the derived class should send the user a prompt.

        :param dialog_context: The dialog context for the current turn of the conversation
        :type dialog_context: :class:`DialogContext`
        :param state: Additional state being persisted for the prompt.
        :type state: :class:`typing.Dict[str, dict]`
        :param options: Options that the prompt started with in the call to :meth:`DialogContext.prompt()`.
        :type options: :class:`PromptOptions`
        :param isRetry: If `true` the users response wasn't recognized and the re-prompt should be sent.
        :type isRetry: bool
        """
        if is_retry and options.retry_prompt:
            options.retry_prompt.input_hint = InputHints.expecting_input
            await context.send_activity(options.retry_prompt)
        elif options.prompt:
            options.prompt.input_hint = InputHints.expecting_input
            await context.send_activity(options.prompt)

    async def on_recognize(  # pylint: disable=unused-argument
        self, context: TurnContext, state: Dict[str, object], options: PromptOptions
    ) -> PromptRecognizerResult:
        """
        When overridden in a derived class, attempts to recognize the incoming activity.

        :param context: Context for the current turn of conversation with the user.
        :type context: :class:`botbuilder.core.TurnContext`
        :param state: Contains state for the current instance of the prompt on the dialog stack.
        :type state: :class:`typing.Dict[str, dict]`
        :param options: A prompt options object
        :type options: :class:`PromptOptions`
        :return result: constructed from the options initially provided in the call to :meth:`async def on_prompt()`
        :rtype result: :class:`PromptRecognizerResult`
        """
        result = PromptRecognizerResult()
        result.succeeded = (True,)
        result.value = context.activity

        return result
