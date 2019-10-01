# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import abstractmethod
import copy
from typing import Dict, List
from botbuilder.core.turn_context import TurnContext
from botbuilder.schema import InputHints, ActivityTypes
from botbuilder.dialogs.choices import (
    Choice,
    ChoiceFactory,
    ChoiceFactoryOptions,
    ListStyle,
)
from botbuilder.schema import Activity
from .prompt_options import PromptOptions
from .prompt_validator_context import PromptValidatorContext
from ..dialog_reason import DialogReason
from ..dialog import Dialog
from ..dialog_instance import DialogInstance
from ..dialog_turn_result import DialogTurnResult
from ..dialog_context import DialogContext


class Prompt(Dialog):
    """ Base class for all prompts."""

    ATTEMPT_COUNT_KEY = "AttemptCount"
    persisted_options = "options"
    persisted_state = "state"

    def __init__(self, dialog_id: str, validator: object = None):
        """Creates a new Prompt instance.
        Parameters
        ----------
        dialog_id
            Unique ID of the prompt within its parent `DialogSet` or
            `ComponentDialog`.
        validator
            (Optional) custom validator used to provide additional validation and
            re-prompting logic for the prompt.
        """
        super(Prompt, self).__init__(dialog_id)

        self._validator = validator

    async def begin_dialog(
        self, dialog_context: DialogContext, options: object = None
    ) -> DialogTurnResult:
        if not dialog_context:
            raise TypeError("Prompt(): dc cannot be None.")
        if not isinstance(options, PromptOptions):
            raise TypeError("Prompt(): Prompt options are required for Prompt dialogs.")
        # Ensure prompts have input hint set
        if options.prompt is not None and not options.prompt.input_hint:
            options.prompt.input_hint = InputHints.expecting_input

        if options.retry_prompt is not None and not options.retry_prompt.input_hint:
            options.retry_prompt.input_hint = InputHints.expecting_input

        # Initialize prompt state
        state = dialog_context.active_dialog.state
        state[self.persisted_options] = options
        state[self.persisted_state] = {}

        # Send initial prompt
        await self.on_prompt(
            dialog_context.context,
            state[self.persisted_state],
            state[self.persisted_options],
            False,
        )

        return Dialog.end_of_turn

    async def continue_dialog(self, dialog_context: DialogContext):
        if not dialog_context:
            raise TypeError("Prompt(): dc cannot be None.")

        # Don't do anything for non-message activities
        if dialog_context.context.activity.type != ActivityTypes.message:
            return Dialog.end_of_turn

        # Perform base recognition
        instance = dialog_context.active_dialog
        state = instance.state[self.persisted_state]
        options = instance.state[self.persisted_options]
        recognized = await self.on_recognize(dialog_context.context, state, options)

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
        else:
            if recognized.succeeded:
                is_valid = True
        # Return recognized value or re-prompt
        if is_valid:
            return await dialog_context.end_dialog(recognized.value)

        if not dialog_context.context.responded:
            await self.on_prompt(dialog_context.context, state, options, True)
        return Dialog.end_of_turn

    async def resume_dialog(
        self, dialog_context: DialogContext, reason: DialogReason, result: object
    ) -> DialogTurnResult:
        # Prompts are typically leaf nodes on the stack but the dev is free to push other dialogs
        # on top of the stack which will result in the prompt receiving an unexpected call to
        # dialog_resume() when the pushed on dialog ends.
        # To avoid the prompt prematurely ending we need to implement this method and
        # simply re-prompt the user.
        await self.reprompt_dialog(dialog_context.context, dialog_context.active_dialog)
        return Dialog.end_of_turn

    async def reprompt_dialog(self, context: TurnContext, instance: DialogInstance):
        state = instance.state[self.persisted_state]
        options = instance.state[self.persisted_options]
        await self.on_prompt(context, state, options, False)

    @abstractmethod
    async def on_prompt(
        self,
        turn_context: TurnContext,
        state: Dict[str, object],
        options: PromptOptions,
        is_retry: bool,
    ):
        pass

    @abstractmethod
    async def on_recognize(
        self,
        turn_context: TurnContext,
        state: Dict[str, object],
        options: PromptOptions,
    ):
        pass

    def append_choices(
        self,
        prompt: Activity,
        channel_id: str,
        choices: List[Choice],
        style: ListStyle,
        options: ChoiceFactoryOptions = None,
    ) -> Activity:
        """
        Helper function to compose an output activity containing a set of choices.

        Parameters:
        -----------
        prompt: The prompt to append the user's choice to.

        channel_id: ID of the channel the prompt is being sent to.

        choices: List of choices to append.

        style: Configured style for the list of choices.

        options: (Optional) options to configure the underlying `ChoiceFactory` call.
        """
        # Get base prompt text (if any)
        text = prompt.text if prompt is not None and prompt.text else ""

        # Create temporary msg
        # TODO: fix once ChoiceFactory complete
        def inline() -> Activity:
            return ChoiceFactory.inline(choices, text, None, options)

        def list_style() -> Activity:
            return ChoiceFactory.list_style(choices, text, None, options)

        def suggested_action() -> Activity:
            return ChoiceFactory.suggested_action(choices, text)

        def hero_card() -> Activity:
            return ChoiceFactory.hero_card(choices, text)

        def list_style_none() -> Activity:
            activity = Activity(type=ActivityTypes.message)
            activity.text = text
            return activity

        def default() -> Activity:
            return ChoiceFactory.for_channel(channel_id, choices, text, None, options)

        # Maps to values in ListStyle Enum
        switcher = {
            0: list_style_none,
            1: default,
            2: inline,
            3: list_style,
            4: suggested_action,
            5: hero_card,
        }

        msg = switcher.get(int(style.value), default)()

        # Update prompt with text, actions and attachments
        if prompt:
            # clone the prompt the set in the options (note ActivityEx has Properties so this is the safest mechanism)
            prompt = copy.copy(prompt)

            prompt.text = msg.text

            if (
                msg.suggested_actions is not None
                and msg.suggested_actions.actions is not None
                and msg.suggested_actions.actions
            ):
                prompt.suggested_actions = msg.suggested_actions

            if msg.attachments:
                if prompt.attachments:
                    prompt.attachments.extend(msg.attachments)
                else:
                    prompt.attachments = msg.attachments

            return prompt

        # TODO: Update to InputHints.ExpectingInput;
        msg.input_hint = None
        return msg
