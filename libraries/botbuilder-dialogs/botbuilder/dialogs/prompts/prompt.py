# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import copy
from typing import Dict
from .prompt_options import PromptOptions
from .prompt_validator_context import PromptValidatorContext
from ..dialog_reason import DialogReason
from ..dialog import Dialog
from ..dialog_instance import DialogInstance
from ..dialog_turn_result import DialogTurnResult
from ..dialog_context import DialogContext
from botbuilder.core.turn_context import TurnContext
from botbuilder.schema import InputHints, ActivityTypes
from botbuilder.dialogs.choices import ChoiceFactory

from abc import abstractmethod
from botbuilder.schema import Activity

""" Base class for all prompts.
"""
class Prompt(Dialog):
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

    async def begin_dialog(self, dc: DialogContext, options: object) -> DialogTurnResult:
        if not dc:
            raise TypeError('Prompt(): dc cannot be None.')
        if not isinstance(options, PromptOptions):
            raise TypeError('Prompt(): Prompt options are required for Prompt dialogs.')
        # Ensure prompts have input hint set
        if options.prompt != None and not options.prompt.input_hint:
            options.prompt.input_hint = InputHints.expecting_input

        if options.retry_prompt != None and not options.prompt.input_hint:
            options.retry_prompt.input_hint = InputHints.expecting_input
       
        # Initialize prompt state
        state = dc.active_dialog.state
        state[self.persisted_options] = options
        state[self.persisted_state] = Dict[str, object]

        # Send initial prompt
        await self.on_prompt(dc.context, state[self.persisted_state], state[self.persisted_options], False)
        
        return Dialog.end_of_turn

    async def continue_dialog(self, dc: DialogContext):
        if not dc:
            raise TypeError('Prompt(): dc cannot be None.')
        
        # Don't do anything for non-message activities
        if dc.context.activity.type != ActivityTypes.message:
            return Dialog.end_of_turn

        # Perform base recognition
        instance = dc.active_dialog
        state = instance.state[self.persisted_state]
        options = instance.state[self.persisted_options]
        recognized = await self.on_recognize(dc.context, state, options)

        # Validate the return value
        is_valid = False
        if self._validator != None:
            prompt_context = PromptValidatorContext(dc.context, recognized, state, options)
            is_valid = await self._validator(prompt_context)
            if options is None:
                options = PromptOptions()
            options.number_of_attempts += 1
        else:
            if recognized.succeeded:
                is_valid = True
        # Return recognized value or re-prompt
        if is_valid:
            return await dc.end_dialog(recognized.value)
        else:
            if not dc.context.responded:
                await self.on_prompt(dc.context, state, options, True)
            return Dialog.end_of_turn
       
    async def resume_dialog(self, dc: DialogContext, reason: DialogReason, result: object) -> DialogTurnResult:
        # Prompts are typically leaf nodes on the stack but the dev is free to push other dialogs
        # on top of the stack which will result in the prompt receiving an unexpected call to
        # dialog_resume() when the pushed on dialog ends.
        # To avoid the prompt prematurely ending we need to implement this method and
        # simply re-prompt the user.
        await self.reprompt_dialog(dc.context, dc.active_dialog)
        return Dialog.end_of_turn        
    
    async def reprompt_dialog(self, turn_context: TurnContext, instance: DialogInstance):
        state = instance.state[self.persisted_state]
        options = instance.state[self.persisted_options]
        await self.on_prompt(turn_context, state, options, False)
    
    @abstractmethod
    async def on_prompt(self, turn_context: TurnContext, state: Dict[str, object], options: PromptOptions, is_retry: bool):
        pass
    
    @abstractmethod
    async def on_recognize(self, turn_context: TurnContext, state: Dict[str, object], options: PromptOptions):
        pass
    
    # TODO: Fix choices to use Choice object when ported.
    # TODO: Fix style to use ListStyle when ported.
    # TODO: Fix options to use ChoiceFactoryOptions object when ported.
    def append_choices(self, prompt: Activity, channel_id: str, choices: object, style: object, options : object = None ) -> Activity:
        # Get base prompt text (if any)
        text = prompt.text if prompt != None and not prompt.text == False else ''
        
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
            activity = Activity()
            activity.text = text
            return activity
        def default() -> Activity:
            return ChoiceFactory.for_channel(channel_id, choices, text, None, options)
        switcher = {
            # ListStyle.inline
            1: inline,
            2: list_style,
            3: suggested_action,
            4: hero_card,
            5: list_style_none
            }
            
        msg = switcher.get(style, default)()

        # Update prompt with text, actions and attachments
        if not prompt:
            # clone the prompt the set in the options (note ActivityEx has Properties so this is the safest mechanism)
            prompt = copy.copy(prompt)

            prompt.text = msg.text

            if (msg.suggested_actions != None and msg.suggested_actions.actions != None
                and len(msg.suggested_actions.actions) > 0):
                prompt.suggested_actions = msg.suggested_actions

            if msg.attachments != None and len(msg.attachments) > 0:
                prompt.attachments = msg.attachments

            return prompt
        else:
            # TODO: Update to InputHints.ExpectingInput;
            msg.input_hint = None
            return msg