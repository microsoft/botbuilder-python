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
    """

    Defines the core behavior of prompt dialogs. Extends the :class:`Dialog` base class.

    .. remarks::
        When the prompt ends, it returns an object that represents the value it was prompted for.
        Use :meth:`DialogSet.add()` or :meth:`ComponentDialog.add_dialog()` to add a prompt to
        a dialog set or component dialog, respectively.

        Use :meth:`DialogContext.prompt()` or :meth:`DialogContext.begin_dialog()` to start the prompt.
        If you start a prompt from a :class:`WaterfallStep` in a :class:`WaterfallDialog`, then the
        prompt result will be available in the next step of the waterfall.
    """

    ATTEMPT_COUNT_KEY = "AttemptCount"
    persisted_options = "options"
    persisted_state = "state"

    def __init__(self, dialog_id: str, validator: object = None):
        """
        Creates a new :class:`Prompt` instance.

        :param dialog_id: Unique Id of the prompt within its parent :class:`DialogSet`
        :class:`ComponentDialog`
        :type dialog_id: str
        :param validator: Optionally provide additional validation and re-prompting logic
        :type validator: Object
        """
        super(Prompt, self).__init__(dialog_id)

        self._validator = validator

    async def begin_dialog(
        self, dialog_context: DialogContext, options: object = None
    ) -> DialogTurnResult:
        """
        Starts a prompt dialog. Called when a prompt dialog is pushed onto the dialog stack and is being activated.

        :param dialog_context: The dialog context for the current turn of the conversation
        :type dialog_context:  :class:`DialogContext`
        :param options: Optional, additional information to pass to the prompt being started
        :type options: Object
        :return: The dialog turn result
        :rtype: :class:`DialogTurnResult`

        .. note::
            The result indicates whether the prompt is still active after the turn has been processed.
        """
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
        """
        Continues a dialog.

        :param dialog_context: The dialog context for the current turn of the conversation
        :type dialog_context:  :class:`DialogContext`
        :return: The dialog turn result
        :rtype: :class:`DialogTurnResult`

        .. remarks::
            Called when a prompt dialog is the active dialog and the user replied with a new activity.

            If the task is successful, the result indicates whether the dialog is still active after
            the turn has been processed by the dialog.

            The prompt generally continues to receive the user's replies until it accepts the
            user's reply as valid input for the prompt.
        """
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
        """
        Resumes a dialog.

        :param dialog_context: The dialog context for the current turn of the conversation.
        :type dialog_context:  :class:`DialogContext`
        :param reason: An enum indicating why the dialog resumed.
        :type reason:  :class:`DialogReason`
        :param result: Optional, value returned from the previous dialog on the stack.
        :type result:  object
        :return: The dialog turn result
        :rtype: :class:`DialogTurnResult`

        .. remarks::
            Called when a prompt dialog resumes being the active dialog on the dialog stack,
            such as when the previous active dialog on the stack completes.

            If the task is successful, the result indicates whether the dialog is still
            active after the turn has been processed by the dialog.

            Prompts are typically leaf nodes on the stack but the dev is free to push other dialogs
            on top of the stack which will result in the prompt receiving an unexpected call to
            :meth:resume_dialog() when the pushed on dialog ends.

            Simply re-prompt the user to avoid that the prompt ends prematurely.

        """
        await self.reprompt_dialog(dialog_context.context, dialog_context.active_dialog)
        return Dialog.end_of_turn

    async def reprompt_dialog(self, context: TurnContext, instance: DialogInstance):
        """
        Reprompts user for input.

        :param context: Context for the current turn of conversation with the user
        :type context:  :class:`botbuilder.core.TurnContext`
        :param instance: The instance of the dialog on the stack
        :type instance:  :class:`DialogInstance`
        :return: A task representing the asynchronous operation

        """
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
        """
        Prompts user for input. When overridden in a derived class, prompts the user for input.

        :param turn_context: Context for the current turn of conversation with the user
        :type turn_context:  :class:`botbuilder.core.TurnContext`
        :param state: Contains state for the current instance of the prompt on the dialog stack
        :type state:  :class:`Dict`
        :param options: A prompt options object constructed from:meth:`DialogContext.prompt()`
        :type options:  :class:`PromptOptions`
        :param is_retry: Determines whether `prompt` or `retry_prompt` should be used
        :type is_retry:  bool

        :return: A task representing the asynchronous operation.

        """

    @abstractmethod
    async def on_recognize(
        self,
        turn_context: TurnContext,
        state: Dict[str, object],
        options: PromptOptions,
    ):
        """
        Recognizes the user's input.

        :param turn_context: Context for the current turn of conversation with the user
        :type turn_context:  :class:`botbuilder.core.TurnContext`
        :param state: Contains state for the current instance of the prompt on the dialog stack
        :type state:  :class:`Dict`
        :param options: A prompt options object constructed from :meth:`DialogContext.prompt()`
        :type options:  :class:`PromptOptions`

        :return: A task representing the asynchronous operation.

        .. note::
            When overridden in a derived class, attempts to recognize the user's input.
        """

    def append_choices(
        self,
        prompt: Activity,
        channel_id: str,
        choices: List[Choice],
        style: ListStyle,
        options: ChoiceFactoryOptions = None,
    ) -> Activity:
        """
        Composes an output activity containing a set of choices.

        :param prompt: The prompt to append the user's choice to
        :type prompt:
        :param channel_id: Id of the channel the prompt is being sent to
        :type channel_id: str
        :param: choices: List of choices to append
        :type choices:  :class:`List`
        :param: style: Configured style for the list of choices
        :type style:  :class:`ListStyle`
        :param: options: Optional formatting options to use when presenting the choices
        :type style: :class:`ChoiceFactoryOptions`

        :return: A task representing the asynchronous operation

        .. remarks::
            If the task is successful, the result contains the updated activity.
            When overridden in a derived class, appends choices to the activity when the user
            is prompted for input. This is an helper function to compose an output activity
            containing a set of choices.

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
