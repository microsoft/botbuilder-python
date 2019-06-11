# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.dialogs.prompts import ActivityPrompt, NumberPrompt, PromptOptions, PromptRecognizerResult
from botbuilder.schema import Activity, InputHints

from botbuilder.core.turn_context import TurnContext
from botbuilder.core.adapters import TestAdapter

class SimpleActivityPrompt(ActivityPrompt):
    pass

class ActivityPromptTests(aiounittest.AsyncTestCase):
    async def test_does_the_things(self):
        my_activity = Activity(type='message', text='I am activity message!')
        my_retry_prompt = Activity(type='message', id='ididretry', text='retry text hurrr')
        options = PromptOptions(prompt=my_activity, retry_prompt=my_retry_prompt)
        activity_promptyy = ActivityPrompt('myId', 'validator thing')

        my_context = TurnContext(TestAdapter(), my_activity)
        my_state = {'stringy': {'nestedkey': 'nestedvalue'} }
        
        await activity_promptyy.on_prompt(my_context, state=my_state, options=options, isRetry=True)

        print('placeholder print')

        pass

    # def test_activity_prompt_with_empty_id_should_fail(self):
    #     empty_id = ''
    #     text_prompt = SimpleActivityPrompt(empty_id, self.validator)
    
    # async def validator(self):
    #     return True
        