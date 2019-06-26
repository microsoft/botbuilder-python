# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
import unittest

from typing import Callable
from botbuilder.dialogs.prompts import (ActivityPrompt, NumberPrompt, PromptOptions, PromptRecognizerResult,
                                        PromptValidatorContext)
from botbuilder.schema import Activity, InputHints, ActivityTypes

from botbuilder.core import ConversationState, MemoryStorage, TurnContext, MessageFactory
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs import DialogSet, DialogTurnStatus


async def validator(prompt_context: PromptValidatorContext):
    tester = unittest.TestCase()
    tester.assertTrue(prompt_context.attempt_count > 0)

    activity = prompt_context.recognized.value

    if activity.type == ActivityTypes.event:
        if int(activity.value) == 2:
            prompt_context.recognized.value = MessageFactory.text(str(activity.value))
            return True
    else:
        await prompt_context.context.send_activity("Please send an 'event'-type Activity with a value of 2.")

    return False


class SimpleActivityPrompt(ActivityPrompt):
    def __init__(self, dialog_id: str, validator: Callable[[PromptValidatorContext], bool]):
        super().__init__(dialog_id, validator)


class ActivityPromptTests(aiounittest.AsyncTestCase):
    async def test_does_the_things(self):
        my_activity = Activity(type='message', text='I am activity message!')
        my_retry_prompt = Activity(type='message', id='ididretry', text='retry text hurrr')
        options = PromptOptions(prompt=my_activity, retry_prompt=my_retry_prompt)
        activity_prompty = ActivityPrompt('myId', 'validator thing')

        my_context = TurnContext(TestAdapter(), my_activity)
        my_state = {'stringy': {'nestedkey': 'nestedvalue'} }
        
        await activity_prompty.on_prompt(my_context, state=my_state, options=options, is_retry=True)

        print('placeholder print')

        pass

    def test_activity_prompt_with_empty_id_should_fail(self):
        empty_id = ''
        with self.assertRaises(TypeError):
            SimpleActivityPrompt(empty_id, validator)

    def test_activity_prompt_with_none_id_should_fail(self):
        none_id = None
        with self.assertRaises(TypeError):
            SimpleActivityPrompt(none_id, validator)

    def test_activity_prompt_with_none_validator_should_fail(self):
        none_validator = None
        with self.assertRaises(TypeError):
            SimpleActivityPrompt('EventActivityPrompt', none_validator)

    async def test_basic_activity_prompt(self):
        async def exec_test(turn_context: TurnContext):
            dc = await dialogs.create_context(turn_context)

            results = await dc.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(prompt=Activity(type=ActivityTypes.message, text='please send an event.'))
                await dc.prompt('EventActivityPrompt', options)
            elif results.status == DialogTurnStatus.Complete:
                await turn_context.send_activity(results.result)

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property('dialog_state')
        dialogs = DialogSet(dialog_state)
        dialogs.add(SimpleActivityPrompt('EventActivityPrompt', validator))

        event_activity = Activity(type=ActivityTypes.event, value=2)

        step1 = await adapter.send('hello')
        step2 = await step1.assert_reply('please send an event.')
        step3 = await step2.send(event_activity)
        await step3.assert_reply('2')
