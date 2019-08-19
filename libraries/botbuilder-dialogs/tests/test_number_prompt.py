# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import Callable

import aiounittest
from recognizers_text import Culture

from botbuilder.dialogs import DialogContext, DialogTurnResult
from botbuilder.dialogs.prompts import (
    NumberPrompt,
    PromptOptions,
    PromptValidatorContext,
)
from botbuilder.core import (
    MemoryStorage,
    ConversationState,
    TurnContext,
    MessageFactory,
)
from botbuilder.core.adapters import TestAdapter, TestFlow
from botbuilder.dialogs import DialogSet, DialogTurnStatus
from botbuilder.schema import Activity, ActivityTypes


class NumberPromptMock(NumberPrompt):
    def __init__(
        self,
        dialog_id: str,
        validator: Callable[[PromptValidatorContext], bool] = None,
        default_locale=None,
    ):
        super().__init__(dialog_id, validator, default_locale)

    async def on_prompt_null_context(self, options: PromptOptions):
        # Should throw TypeError
        await self.on_prompt(
            turn_context=None, state=None, options=options, is_retry=False
        )

    async def on_prompt_null_options(self, dialog_context: DialogContext):
        # Should throw TypeError
        await self.on_prompt(
            dialog_context.context, state=None, options=None, is_retry=False
        )

    async def on_recognize_null_context(self):
        # Should throw TypeError
        await self.on_recognize(turn_context=None, state=None, options=None)


class NumberPromptTests(aiounittest.AsyncTestCase):
    def test_empty_id_should_fail(self):
        # pylint: disable=no-value-for-parameter
        empty_id = ""
        self.assertRaises(TypeError, lambda: NumberPrompt(empty_id))

    def test_none_id_should_fail(self):
        # pylint: disable=no-value-for-parameter
        self.assertRaises(TypeError, lambda: NumberPrompt(dialog_id=None))

    async def test_with_null_turn_context_should_fail(self):
        number_prompt_mock = NumberPromptMock("NumberPromptMock")

        options = PromptOptions(
            prompt=Activity(type=ActivityTypes.message, text="Please send a number.")
        )

        with self.assertRaises(TypeError):
            await number_prompt_mock.on_prompt_null_context(options)

    async def test_on_prompt_with_null_options_fails(self):
        conver_state = ConversationState(MemoryStorage())
        dialog_state = conver_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        number_prompt_mock = NumberPromptMock(
            dialog_id="NumberPromptMock", validator=None, default_locale=Culture.English
        )
        dialogs.add(number_prompt_mock)

        with self.assertRaises(TypeError):
            await number_prompt_mock.on_recognize_null_context()

    async def test_number_prompt(self):
        # Create new ConversationState with MemoryStorage and register the state as middleware.
        conver_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and register the WaterfallDialog.
        dialog_state = conver_state.create_property("dialogState")

        dialogs = DialogSet(dialog_state)

        # Create and add number prompt to DialogSet.
        number_prompt = NumberPrompt("NumberPrompt", None, Culture.English)
        dialogs.add(number_prompt)

        async def exec_test(turn_context: TurnContext) -> None:
            dialog_context = await dialogs.create_context(turn_context)
            results = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                await dialog_context.begin_dialog(
                    "NumberPrompt",
                    PromptOptions(
                        prompt=MessageFactory.text("Enter quantity of cable")
                    ),
                )
            else:
                if results.status == DialogTurnStatus.Complete:
                    number_result = results.result
                    await turn_context.send_activity(
                        MessageFactory.text(
                            f"You asked me for '{number_result}' meters of cable."
                        )
                    )

            await conver_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        test_flow = TestFlow(None, adapter)

        test_flow2 = await test_flow.send("Hello")
        test_flow3 = await test_flow2.assert_reply("Enter quantity of cable")
        test_flow4 = await test_flow3.send("Give me twenty meters of cable")
        await test_flow4.assert_reply("You asked me for '20' meters of cable.")

    async def test_number_prompt_retry(self):
        async def exec_test(turn_context: TurnContext) -> None:
            dialog_context: DialogContext = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text="Enter a number."),
                    retry_prompt=Activity(
                        type=ActivityTypes.message, text="You must enter a number."
                    ),
                )
                await dialog_context.prompt("NumberPrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                number_result = results.result
                await turn_context.send_activity(
                    MessageFactory.text(f"Bot received the number '{number_result}'.")
                )

            await convo_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)
        number_prompt = NumberPrompt(
            dialog_id="NumberPrompt", validator=None, default_locale=Culture.English
        )
        dialogs.add(number_prompt)

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("Enter a number.")
        step3 = await step2.send("hello")
        step4 = await step3.assert_reply("You must enter a number.")
        step5 = await step4.send("64")
        await step5.assert_reply("Bot received the number '64'.")

    async def test_number_uses_locale_specified_in_constructor(self):
        # Create new ConversationState with MemoryStorage and register the state as middleware.
        conver_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and register the WaterfallDialog.
        dialog_state = conver_state.create_property("dialogState")

        dialogs = DialogSet(dialog_state)

        # Create and add number prompt to DialogSet.
        number_prompt = NumberPrompt(
            "NumberPrompt", None, default_locale=Culture.Spanish
        )
        dialogs.add(number_prompt)

        async def exec_test(turn_context: TurnContext) -> None:

            dialog_context = await dialogs.create_context(turn_context)
            results = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                await dialog_context.begin_dialog(
                    "NumberPrompt",
                    PromptOptions(
                        prompt=MessageFactory.text(
                            "How much money is in your gaming account?"
                        )
                    ),
                )
            else:
                if results.status == DialogTurnStatus.Complete:
                    number_result = results.result
                    await turn_context.send_activity(
                        MessageFactory.text(
                            f"You say you have ${number_result} in your gaming account."
                        )
                    )

            await conver_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        test_flow = TestFlow(None, adapter)

        test_flow2 = await test_flow.send("Hello")
        test_flow3 = await test_flow2.assert_reply(
            "How much money is in your gaming account?"
        )
        test_flow4 = await test_flow3.send("I've got $1.200.555,42 in my account.")
        await test_flow4.assert_reply(
            "You say you have $1200555.42 in your gaming account."
        )

    async def test_number_prompt_validator(self):
        async def exec_test(turn_context: TurnContext) -> None:
            dialog_context = await dialogs.create_context(turn_context)
            results = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text="Enter a number."),
                    retry_prompt=Activity(
                        type=ActivityTypes.message,
                        text="You must enter a positive number less than 100.",
                    ),
                )
                await dialog_context.prompt("NumberPrompt", options)

            elif results.status == DialogTurnStatus.Complete:
                number_result = int(results.result)
                await turn_context.send_activity(
                    MessageFactory.text(f"Bot received the number '{number_result}'.")
                )

            await conver_state.save_changes(turn_context)

        # Create new ConversationState with MemoryStorage and register the state as middleware.
        conver_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and register the WaterfallDialog.
        dialog_state = conver_state.create_property("dialogState")

        dialogs = DialogSet(dialog_state)

        # Create and add number prompt to DialogSet.
        async def validator(prompt_context: PromptValidatorContext):
            result = prompt_context.recognized.value

            if 0 < result < 100:
                return True

            return False

        number_prompt = NumberPrompt(
            "NumberPrompt", validator, default_locale=Culture.English
        )
        dialogs.add(number_prompt)

        adapter = TestAdapter(exec_test)

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("Enter a number.")
        step3 = await step2.send("150")
        step4 = await step3.assert_reply(
            "You must enter a positive number less than 100."
        )
        step5 = await step4.send("64")
        await step5.assert_reply("Bot received the number '64'.")

    async def test_float_number_prompt(self):
        async def exec_test(turn_context: TurnContext) -> None:
            dialog_context = await dialogs.create_context(turn_context)
            results = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text="Enter a number.")
                )
                await dialog_context.prompt("NumberPrompt", options)

            elif results.status == DialogTurnStatus.Complete:
                number_result = float(results.result)
                await turn_context.send_activity(
                    MessageFactory.text(f"Bot received the number '{number_result}'.")
                )

            await conver_state.save_changes(turn_context)

        # Create new ConversationState with MemoryStorage and register the state as middleware.
        conver_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and register the WaterfallDialog.
        dialog_state = conver_state.create_property("dialogState")

        dialogs = DialogSet(dialog_state)

        # Create and add number prompt to DialogSet.
        number_prompt = NumberPrompt(
            "NumberPrompt", validator=None, default_locale=Culture.English
        )
        dialogs.add(number_prompt)

        adapter = TestAdapter(exec_test)

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("Enter a number.")
        step3 = await step2.send("3.14")
        await step3.assert_reply("Bot received the number '3.14'.")

    async def test_number_prompt_uses_locale_specified_in_activity(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)
            results = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text="Enter a number.")
                )
                await dialog_context.prompt("NumberPrompt", options)

            elif results.status == DialogTurnStatus.Complete:
                number_result = float(results.result)
                self.assertEqual(3.14, number_result)

            await conver_state.save_changes(turn_context)

        conver_state = ConversationState(MemoryStorage())
        dialog_state = conver_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        number_prompt = NumberPrompt("NumberPrompt", None, None)
        dialogs.add(number_prompt)

        adapter = TestAdapter(exec_test)

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("Enter a number.")
        await step2.send(
            Activity(type=ActivityTypes.message, text="3,14", locale=Culture.Spanish)
        )

    async def test_number_prompt_defaults_to_en_us_culture(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)
            results = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(type=ActivityTypes.message, text="Enter a number.")
                )
                await dialog_context.prompt("NumberPrompt", options)

            elif results.status == DialogTurnStatus.Complete:
                number_result = float(results.result)
                await turn_context.send_activity(
                    MessageFactory.text(f"Bot received the number '{number_result}'.")
                )

            await conver_state.save_changes(turn_context)

        conver_state = ConversationState(MemoryStorage())
        dialog_state = conver_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        number_prompt = NumberPrompt("NumberPrompt")
        dialogs.add(number_prompt)

        adapter = TestAdapter(exec_test)

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("Enter a number.")
        step3 = await step2.send("3.14")
        await step3.assert_reply("Bot received the number '3.14'.")
