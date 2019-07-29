# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.core import (
    ConversationState,
    MemoryStorage,
    TurnContext,
    MessageFactory,
)
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs import DialogSet, DialogTurnResult, DialogTurnStatus
from botbuilder.dialogs.choices import ChoiceFactoryOptions, ListStyle
from botbuilder.dialogs.prompts import ConfirmPrompt
from botbuilder.dialogs.prompts import PromptOptions
from botbuilder.schema import Activity, ActivityTypes


class ConfirmPromptTest(aiounittest.AsyncTestCase):
    def test_confirm_prompt_with_empty_id_should_fail(self):
        empty_id = ""

        with self.assertRaises(TypeError):
            ConfirmPrompt(empty_id)

    def test_confirm_prompt_with_none_id_should_fail(self):
        none_id = None

        with self.assertRaises(TypeError):
            ConfirmPrompt(none_id)

    async def test_confirm_prompt(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text="Please confirm.")
                )
                await dialog_context.prompt("ConfirmPrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                message_text = "Confirmed" if results.result else "Not confirmed"
                await turn_context.send_activity(MessageFactory.text(message_text))

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create new ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet, and ChoicePrompt.
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)
        confirm_prompt = ConfirmPrompt("ConfirmPrompt", default_locale="English")
        dialogs.add(confirm_prompt)

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("Please confirm. (1) Yes or (2) No")
        step3 = await step2.send("yes")
        await step3.assert_reply("Confirmed")

    async def test_confirm_prompt_retry(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text="Please confirm."),
                    retry_prompt=Activity(
                        type=ActivityTypes.message,
                        text="Please confirm, say 'yes' or 'no' or something like that.",
                    ),
                )
                await dialog_context.prompt("ConfirmPrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                message_text = "Confirmed" if results.result else "Not confirmed"
                await turn_context.send_activity(MessageFactory.text(message_text))

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create new ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet, and ChoicePrompt.
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)
        confirm_prompt = ConfirmPrompt("ConfirmPrompt", default_locale="English")
        dialogs.add(confirm_prompt)

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("Please confirm. (1) Yes or (2) No")
        step3 = await step2.send("lala")
        step4 = await step3.assert_reply(
            "Please confirm, say 'yes' or 'no' or something like that. (1) Yes or (2) No"
        )
        step5 = await step4.send("no")
        await step5.assert_reply("Not confirmed")

    async def test_confirm_prompt_no_options(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                await dialog_context.prompt("ConfirmPrompt", PromptOptions())
            elif results.status == DialogTurnStatus.Complete:
                message_text = "Confirmed" if results.result else "Not confirmed"
                await turn_context.send_activity(MessageFactory.text(message_text))

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create new ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet, and ChoicePrompt.
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)
        confirm_prompt = ConfirmPrompt("ConfirmPrompt", default_locale="English")
        dialogs.add(confirm_prompt)

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply(" (1) Yes or (2) No")
        step3 = await step2.send("lala")
        step4 = await step3.assert_reply(" (1) Yes or (2) No")
        step5 = await step4.send("no")
        await step5.assert_reply("Not confirmed")

    async def test_confirm_prompt_choice_options_numbers(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text="Please confirm."),
                    retry_prompt=Activity(
                        type=ActivityTypes.message,
                        text="Please confirm, say 'yes' or 'no' or something like that.",
                    ),
                )
                await dialog_context.prompt("ConfirmPrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                message_text = "Confirmed" if results.result else "Not confirmed"
                await turn_context.send_activity(MessageFactory.text(message_text))

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create new ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet, and ChoicePrompt.
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)
        confirm_prompt = ConfirmPrompt("ConfirmPrompt", default_locale="English")
        confirm_prompt.choice_options = ChoiceFactoryOptions(include_numbers=True)
        confirm_prompt.style = ListStyle.in_line
        dialogs.add(confirm_prompt)

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("Please confirm. (1) Yes or (2) No")
        step3 = await step2.send("lala")
        step4 = await step3.assert_reply(
            "Please confirm, say 'yes' or 'no' or something like that. (1) Yes or (2) No"
        )
        step5 = await step4.send("2")
        await step5.assert_reply("Not confirmed")

    async def test_confirm_prompt_choice_options_multiple_attempts(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text="Please confirm."),
                    retry_prompt=Activity(
                        type=ActivityTypes.message,
                        text="Please confirm, say 'yes' or 'no' or something like that.",
                    ),
                )
                await dialog_context.prompt("ConfirmPrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                message_text = "Confirmed" if results.result else "Not confirmed"
                await turn_context.send_activity(MessageFactory.text(message_text))

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create new ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet, and ChoicePrompt.
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)
        confirm_prompt = ConfirmPrompt("ConfirmPrompt", default_locale="English")
        confirm_prompt.choice_options = ChoiceFactoryOptions(include_numbers=True)
        confirm_prompt.style = ListStyle.in_line
        dialogs.add(confirm_prompt)

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("Please confirm. (1) Yes or (2) No")
        step3 = await step2.send("lala")
        step4 = await step3.assert_reply(
            "Please confirm, say 'yes' or 'no' or something like that. (1) Yes or (2) No"
        )
        step5 = await step4.send("what")
        step6 = await step5.assert_reply(
            "Please confirm, say 'yes' or 'no' or something like that. (1) Yes or (2) No"
        )
        step7 = await step6.send("2")
        await step7.assert_reply("Not confirmed")

    async def test_confirm_prompt_options_no_numbers(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text="Please confirm."),
                    retry_prompt=Activity(
                        type=ActivityTypes.message,
                        text="Please confirm, say 'yes' or 'no' or something like that.",
                    ),
                )
                await dialog_context.prompt("ConfirmPrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                message_text = "Confirmed" if results.result else "Not confirmed"
                await turn_context.send_activity(MessageFactory.text(message_text))

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create new ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet, and ChoicePrompt.
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)
        confirm_prompt = ConfirmPrompt("ConfirmPrompt", default_locale="English")
        confirm_prompt.choice_options = ChoiceFactoryOptions(
            include_numbers=False, inline_separator="~"
        )
        dialogs.add(confirm_prompt)

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("Please confirm. Yes or No")
        step3 = await step2.send("2")
        step4 = await step3.assert_reply(
            "Please confirm, say 'yes' or 'no' or something like that. Yes or No"
        )
        step5 = await step4.send("no")
        await step5.assert_reply("Not confirmed")
