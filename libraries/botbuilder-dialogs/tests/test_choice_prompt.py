# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

import aiounittest

from botbuilder.core import ConversationState, MemoryStorage
from botbuilder.dialogs.choices import Choice
from botbuilder.dialogs.prompts import ChoicePrompt

_color_choices: List[Choice] = [
    Choice(value='red'),
    Choice(value='green'),
    Choice(value='blue')
]

class ChoicePromptTest(aiounittest.AsyncTestCase):

    def test_choice_prompt_with_empty_id_should_fail(self):
        empty_id = ''

        with self.assertRaises(TypeError):
            ChoicePrompt(empty_id)
    
    def test_choice_prompt_with_none_id_should_fail(self):
        none_id = None

        with self.assertRaises(TypeError):
            ChoicePrompt(none_id)
    
    async def test_choice_prompt_with_card_action_and_no_value_should_not_fail(self):
        # convo_state = ConversationState(MemoryStorage())
        # dialog_state = convo_state.create_property('dialogState')
        pass
    
    async def test_should_send_prompt(self):
        pass
    
    async def test_should_send_prompt_as_an_inline_list(self):
        pass
    
    async def test_should_send_prompt_as_a_numbered_list(self):
        pass
    
    async def test_should_send_prompt_using_suggested_actions(self):
        pass
    
    async def test_should_send_prompt_using_hero_card(self):
        pass
    
    async def test_should_send_prompt_without_adding_a_list(self):
        pass
    
    async def test_should_send_prompt_without_adding_a_list_but_adding_ssml(self):
        pass
    
    async def test_should_recognize_a_choice(self):
        pass
    
    async def test_shold_not_recognize_other_text(self):
        pass
    
    async def test_should_call_custom_validator(self):
        pass
    
    async def test_should_use_choice_style_if_present(self):
        pass