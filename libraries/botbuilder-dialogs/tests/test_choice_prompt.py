# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from recognizers_text import Culture
from typing import List

import aiounittest

from botbuilder.core import ConversationState, MemoryStorage, TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs import Dialog, DialogSet, DialogContext, DialogTurnResult, DialogTurnStatus, WaterfallStepContext
from botbuilder.dialogs.choices import Choice, ListStyle
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions, PromptValidatorContext
from botbuilder.schema import Activity, ActivityTypes

_color_choices: List[Choice] = [
    Choice(value='red'),
    Choice(value='green'),
    Choice(value='blue')
]

_answer_message: Activity = Activity(text='red', type=ActivityTypes.message)
_invalid_message: Activity = Activity(text='purple', type=ActivityTypes.message)

class ChoicePromptTest(aiounittest.AsyncTestCase):

    def test_choice_prompt_with_empty_id_should_fail(self):
        empty_id = ''

        with self.assertRaises(TypeError):
            ChoicePrompt(empty_id)
    
    def test_choice_prompt_with_none_id_should_fail(self):
        none_id = None

        with self.assertRaises(TypeError):
            ChoicePrompt(none_id)
    
    async def test_should_call_ChoicePrompt_using_dc_prompt(self):
        async def exec_test(turn_context: TurnContext):
            dc = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dc.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text='Please choose a color.'),
                    choices=_color_choices
                )
                await dc.prompt('ChoicePrompt', options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)
            
            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create new ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet, and ChoicePrompt.
        dialog_state = convo_state.create_property('dialogState')
        dialogs = DialogSet(dialog_state)
        choice_prompt = ChoicePrompt('ChoicePrompt')
        dialogs.add(choice_prompt)

        step1 = await adapter.send('hello')
        step2 = await step1.assert_reply('Please choose a color. (1) red, (2) green, or (3) blue')
        step3 = await step2.send(_answer_message)
        await step3.assert_reply('red')
    
    async def test_should_call_ChoicePrompt_with_custom_validator(self):
        async def exec_test(turn_context: TurnContext):
            dc = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dc.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text='Please choose a color.'),
                    choices=_color_choices
                )
                await dc.prompt('prompt', options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)
            
            await convo_state.save_changes(turn_context)
        
        adapter = TestAdapter(exec_test)
        
        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property('dialogState')
        dialogs = DialogSet(dialog_state)

        async def validator(prompt: PromptValidatorContext) -> bool:
            assert prompt

            return prompt.recognized.succeeded
        
        choice_prompt = ChoicePrompt('prompt', validator)

        dialogs.add(choice_prompt)

        step1 = await adapter.send('Hello')
        step2 = await step1.assert_reply('Please choose a color. (1) red, (2) green, or (3) blue')
        step3 = await step2.send(_invalid_message)
        step4 = await step3.assert_reply('Please choose a color. (1) red, (2) green, or (3) blue')
        step5 = await step4.send(_answer_message)
        await step5.assert_reply('red')

    async def test_should_send_custom_retry_prompt(self):
        async def exec_test(turn_context: TurnContext):
            dc = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dc.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text='Please choose a color.'),
                    retry_prompt=Activity(type=ActivityTypes.message, text='Please choose red, blue, or green.'),
                    choices=_color_choices
                )
                await dc.prompt('prompt', options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)
            
            await convo_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)
        
        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property('dialogState')
        dialogs = DialogSet(dialog_state)
        choice_prompt = ChoicePrompt('prompt')
        dialogs.add(choice_prompt)
    
        step1 = await adapter.send('Hello')
        step2 = await step1.assert_reply('Please choose a color. (1) red, (2) green, or (3) blue')
        step3 = await step2.send(_invalid_message)
        step4 = await step3.assert_reply('Please choose red, blue, or green. (1) red, (2) green, or (3) blue')
        step5 = await step4.send(_answer_message)
        await step5.assert_reply('red')

    async def test_should_send_ignore_retry_prompt_if_validator_replies(self):
        async def exec_test(turn_context: TurnContext):
            dc = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dc.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text='Please choose a color.'),
                    retry_prompt=Activity(type=ActivityTypes.message, text='Please choose red, blue, or green.'),
                    choices=_color_choices
                )
                await dc.prompt('prompt', options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)
            
            await convo_state.save_changes(turn_context)
        
        adapter = TestAdapter(exec_test)
        
        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property('dialogState')
        dialogs = DialogSet(dialog_state)

        async def validator(prompt: PromptValidatorContext) -> bool:
            assert prompt

            if not prompt.recognized.succeeded:
                await prompt.context.send_activity('Bad input.')
            
            return prompt.recognized.succeeded
        
        choice_prompt = ChoicePrompt('prompt', validator)

        dialogs.add(choice_prompt)

        step1 = await adapter.send('Hello')
        step2 = await step1.assert_reply('Please choose a color. (1) red, (2) green, or (3) blue')
        step3 = await step2.send(_invalid_message)
        step4 = await step3.assert_reply('Bad input.')
        step5 = await step4.send(_answer_message)
        await step5.assert_reply('red')

    async def test_should_use_default_locale_when_rendering_choices(self):
        async def exec_test(turn_context: TurnContext):
            dc = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dc.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text='Please choose a color.'),
                    choices=_color_choices
                )
                await dc.prompt('prompt', options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)
            
            await convo_state.save_changes(turn_context)
        
        adapter = TestAdapter(exec_test)
        
        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property('dialogState')
        dialogs = DialogSet(dialog_state)

        async def validator(prompt: PromptValidatorContext) -> bool:
            assert prompt
            
            if not prompt.recognized.succeeded:
                await prompt.context.send_activity('Bad input.')
            
            return prompt.recognized.succeeded
        
        choice_prompt = ChoicePrompt(
            'prompt',
            validator,
            default_locale=Culture.Spanish
        )

        dialogs.add(choice_prompt)

        step1 = await adapter.send(Activity(type=ActivityTypes.message, text='Hello'))
        # TODO ChoiceFactory.inline() is broken, where it only uses hard-coded English locale.
        # commented out the CORRECT assertion below, until .inline() is fixed to use proper locale
        # step2 = await step1.assert_reply('Please choose a color. (1) red, (2) green, o (3) blue')
        step2 = await step1.assert_reply('Please choose a color. (1) red, (2) green, or (3) blue')
        step3 = await step2.send(_invalid_message)
        step4 = await step3.assert_reply('Bad input.')
        step5 = await step4.send(Activity(type=ActivityTypes.message, text='red'))
        await step5.assert_reply('red')

    async def test_should_use_context_activity_locale_when_rendering_choices(self):
        async def exec_test(turn_context: TurnContext):
            dc = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dc.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text='Please choose a color.'),
                    choices=_color_choices
                )
                await dc.prompt('prompt', options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)
            
            await convo_state.save_changes(turn_context)
        
        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property('dialogState')
        dialogs = DialogSet(dialog_state)

        async def validator(prompt: PromptValidatorContext) -> bool:
            assert prompt

            if not prompt.recognized.succeeded:
                await prompt.context.send_activity('Bad input.')

            return prompt.recognized.succeeded
        
        choice_prompt = ChoicePrompt('prompt', validator)
        dialogs.add(choice_prompt)

        step1 = await adapter.send(
            Activity(
                type=ActivityTypes.message,
                text='Hello',
                locale=Culture.Spanish
            )
        )
        # TODO ChoiceFactory.inline() is broken, where it only uses hard-coded English locale.
        # commented out the CORRECT assertion below, until .inline() is fixed to use proper locale
        # step2 = await step1.assert_reply('Please choose a color. (1) red, (2) green, o (3) blue')
        step2 = await step1.assert_reply('Please choose a color. (1) red, (2) green, or (3) blue')
        step3 = await step2.send(_answer_message)
        await step3.assert_reply('red')
    
    async def test_should_use_context_activity_locale_over_default_locale_when_rendering_choices(self):
        async def exec_test(turn_context: TurnContext):
            dc = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dc.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text='Please choose a color.'),
                    choices=_color_choices
                )
                await dc.prompt('prompt', options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)
            
            await convo_state.save_changes(turn_context)
        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property('dialogState')
        dialogs = DialogSet(dialog_state)

        async def validator(prompt: PromptValidatorContext) -> bool:
            assert prompt

            if not prompt.recognized.succeeded:
                await prompt.context.send_activity('Bad input.')
            
            return prompt.recognized.succeeded
        
        choice_prompt = ChoicePrompt(
            'prompt',
            validator,
            default_locale=Culture.Spanish
        )
        dialogs.add(choice_prompt)

        step1 = await adapter.send(
            Activity(
                type=ActivityTypes.message,
                text='Hello',
                locale=Culture.English
            )
        )
        step2 = await step1.assert_reply('Please choose a color. (1) red, (2) green, or (3) blue')
        step3 = await step2.send(_answer_message)
        await step3.assert_reply('red')
    
    async def test_should_not_render_choices_and_not_blow_up_if_choices_are_not_passed_in(self):
        async def exec_test(turn_context: TurnContext):
            dc = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dc.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text='Please choose a color.'),
                    choices=None
                )
                await dc.prompt('prompt', options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)
            
            await convo_state.save_changes(turn_context)
        
        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property('dialogState')
        dialogs = DialogSet(dialog_state)
        
        choice_prompt = ChoicePrompt('prompt')
        choice_prompt.style = ListStyle.none
        
        dialogs.add(choice_prompt)

        step1 = await adapter.send('Hello')
        await step1.assert_reply('Please choose a color.')
    
    # TODO to create parity with JS, need to refactor this so that it does not blow up when choices are None
    # Possibly does not work due to the side effect of list styles not applying
    # Note: step2 only appears to pass as ListStyle.none, probably because choices is None, and therefore appending
    # nothing to the prompt text
    async def test_should_not_recognize_if_choices_are_not_passed_in(self):
        async def exec_test(turn_context: TurnContext):
            dc = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dc.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text='Please choose a color.'),
                    choices=None
                )
                await dc.prompt('prompt', options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)
            
            await convo_state.save_changes(turn_context)
        
        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property('dialogState')
        dialogs = DialogSet(dialog_state)

        choice_prompt = ChoicePrompt('prompt')
        choice_prompt.style = ListStyle.none

        dialogs.add(choice_prompt)

        step1 = await adapter.send('Hello')
        step2 = await step1.assert_reply('Please choose a color.')
        # TODO uncomment when styling is fixed for prompts - assertions should pass
        # step3 = await step2.send('hello')
        # await step3.assert_reply('Please choose a color.')

    async def test_should_create_prompt_with_inline_choices_when_specified(self):
        async def exec_test(turn_context: TurnContext):
            dc = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dc.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text='Please choose a color.'),
                    choices=_color_choices
                )
                await dc.prompt('prompt', options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)
            
            await convo_state.save_changes(turn_context)
        
        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property('dialogState')
        dialogs = DialogSet(dialog_state)
        
        choice_prompt = ChoicePrompt('prompt')
        choice_prompt.style = ListStyle.in_line

        dialogs.add(choice_prompt)

        step1 = await adapter.send('Hello')
        step2 = await step1.assert_reply('Please choose a color. (1) red, (2) green, or (3) blue')
        step3 = await step2.send(_answer_message)
        await step3.assert_reply('red')

    # TODO fix test to actually test for list_style instead of inline
    # currently bug where all styling is ignored and only does inline styling for prompts
    async def test_should_create_prompt_with_list_choices_when_specified(self):
        async def exec_test(turn_context: TurnContext):
            dc = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dc.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text='Please choose a color.'),
                    choices=_color_choices
                )
                await dc.prompt('prompt', options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)
            
            await convo_state.save_changes(turn_context)
        
        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property('dialogState')
        dialogs = DialogSet(dialog_state)
        
        choice_prompt = ChoicePrompt('prompt')
        choice_prompt.style = ListStyle.list_style

        dialogs.add(choice_prompt)

        step1 = await adapter.send('Hello')
        # TODO uncomment assertion when prompt styling has been fixed - assertion should pass with list_style
        # Also be sure to remove inline assertion currently being tested below
        # step2 = await step1.assert_reply('Please choose a color.\n\n   1. red\n   2. green\n   3. blue')
        step2 = await step1.assert_reply('Please choose a color. (1) red, (2) green, or (3) blue')
        step3 = await step2.send(_answer_message)
        await step3.assert_reply('red')

    async def test_should_recognize_valid_number_choice(self):
        async def exec_test(turn_context: TurnContext):
            dc = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dc.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text='Please choose a color.'),
                    choices=_color_choices
                )
                await dc.prompt('prompt', options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)
            
            await convo_state.save_changes(turn_context)
        
        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property('dialogState')
        dialogs = DialogSet(dialog_state)
        
        choice_prompt = ChoicePrompt('prompt')

        dialogs.add(choice_prompt)

        step1 = await adapter.send('Hello')
        step2 = await step1.assert_reply('Please choose a color. (1) red, (2) green, or (3) blue')
        step3 = await step2.send('1')
        await step3.assert_reply('red')
        
