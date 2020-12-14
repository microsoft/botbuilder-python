# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import unittest
import aiounittest

from botbuilder.dialogs.prompts import (
    ActivityPrompt,
    PromptOptions,
    PromptValidatorContext,
)
from botbuilder.schema import Activity, ActivityTypes

from botbuilder.core import (
    ConversationState,
    MemoryStorage,
    TurnContext,
    MessageFactory,
)
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs import DialogSet, DialogTurnStatus, DialogReason


async def validator(prompt_context: PromptValidatorContext):
    tester = unittest.TestCase()
    tester.assertTrue(prompt_context.attempt_count > 0)

    activity = prompt_context.recognized.value

    if activity.type == ActivityTypes.event:
        if int(activity.value) == 2:
            prompt_context.recognized.value = MessageFactory.text(str(activity.value))
            return True
    else:
        await prompt_context.context.send_activity(
            "Please send an 'event'-type Activity with a value of 2."
        )

    return False


class SimpleActivityPrompt(ActivityPrompt):
    pass


class ActivityPromptTests(aiounittest.AsyncTestCase):
    def test_activity_prompt_with_empty_id_should_fail(self):
        empty_id = ""
        with self.assertRaises(TypeError):
            SimpleActivityPrompt(empty_id, validator)

    def test_activity_prompt_with_none_id_should_fail(self):
        none_id = None
        with self.assertRaises(TypeError):
            SimpleActivityPrompt(none_id, validator)

    def test_activity_prompt_with_none_validator_should_fail(self):
        none_validator = None
        with self.assertRaises(TypeError):
            SimpleActivityPrompt("EventActivityPrompt", none_validator)

    async def test_basic_activity_prompt(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="please send an event."
                    )
                )
                await dialog_context.prompt("EventActivityPrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                await turn_context.send_activity(results.result)

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialog_state")
        dialogs = DialogSet(dialog_state)
        dialogs.add(SimpleActivityPrompt("EventActivityPrompt", validator))

        event_activity = Activity(type=ActivityTypes.event, value=2)

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("please send an event.")
        step3 = await step2.send(event_activity)
        await step3.assert_reply("2")

    async def test_retry_activity_prompt(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="please send an event."
                    )
                )
                await dialog_context.prompt("EventActivityPrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                await turn_context.send_activity(results.result)

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialog_state")
        dialogs = DialogSet(dialog_state)
        dialogs.add(SimpleActivityPrompt("EventActivityPrompt", validator))

        event_activity = Activity(type=ActivityTypes.event, value=2)

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("please send an event.")
        step3 = await step2.send("hello again")
        step4 = await step3.assert_reply(
            "Please send an 'event'-type Activity with a value of 2."
        )
        step5 = await step4.send(event_activity)
        await step5.assert_reply("2")

    async def test_activity_prompt_should_return_dialog_end_if_validation_failed(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="please send an event."
                    ),
                    retry_prompt=Activity(
                        type=ActivityTypes.message, text="event not received."
                    ),
                )
                await dialog_context.prompt("EventActivityPrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                await turn_context.send_activity(results.result)

            await convo_state.save_changes(turn_context)

        async def aux_validator(prompt_context: PromptValidatorContext):
            assert prompt_context, "Validator missing prompt_context"
            return False

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialog_state")
        dialogs = DialogSet(dialog_state)
        dialogs.add(SimpleActivityPrompt("EventActivityPrompt", aux_validator))

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("please send an event.")
        step3 = await step2.send("test")
        await step3.assert_reply("event not received.")

    async def test_activity_prompt_resume_dialog_should_return_dialog_end(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="please send an event."
                    )
                )
                await dialog_context.prompt("EventActivityPrompt", options)

            second_results = await event_prompt.resume_dialog(
                dialog_context, DialogReason.NextCalled
            )

            assert (
                second_results.status == DialogTurnStatus.Waiting
            ), "resume_dialog did not returned Dialog.EndOfTurn"

            await convo_state.save_changes(turn_context)

        async def aux_validator(prompt_context: PromptValidatorContext):
            assert prompt_context, "Validator missing prompt_context"
            return False

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialog_state")
        dialogs = DialogSet(dialog_state)
        event_prompt = SimpleActivityPrompt("EventActivityPrompt", aux_validator)
        dialogs.add(event_prompt)

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("please send an event.")
        await step2.assert_reply("please send an event.")

    async def test_activity_prompt_onerror_should_return_dialogcontext(self):
        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialog_state")
        dialogs = DialogSet(dialog_state)
        dialogs.add(SimpleActivityPrompt("EventActivityPrompt", validator))

        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="please send an event."
                    )
                )

                try:
                    await dialog_context.prompt("EventActivityPrompt", options)
                    await dialog_context.prompt("Non existent id", options)
                except Exception as err:
                    self.assertIsNotNone(
                        err.data["DialogContext"]  # pylint: disable=no-member
                    )
                    self.assertEqual(
                        err.data["DialogContext"][  # pylint: disable=no-member
                            "active_dialog"
                        ],
                        "EventActivityPrompt",
                    )
                else:
                    raise Exception("Should have thrown an error.")

            elif results.status == DialogTurnStatus.Complete:
                await turn_context.send_activity(results.result)

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        await adapter.send("hello")

    async def test_activity_replace_dialog_onerror_should_return_dialogcontext(self):
        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialog_state")
        dialogs = DialogSet(dialog_state)
        dialogs.add(SimpleActivityPrompt("EventActivityPrompt", validator))

        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="please send an event."
                    )
                )

                try:
                    await dialog_context.prompt("EventActivityPrompt", options)
                    await dialog_context.replace_dialog("Non existent id", options)
                except Exception as err:
                    self.assertIsNotNone(
                        err.data["DialogContext"]  # pylint: disable=no-member
                    )
                else:
                    raise Exception("Should have thrown an error.")

            elif results.status == DialogTurnStatus.Complete:
                await turn_context.send_activity(results.result)

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        await adapter.send("hello")
