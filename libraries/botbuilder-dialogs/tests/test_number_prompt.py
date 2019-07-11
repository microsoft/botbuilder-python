# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import aiounittest
from botbuilder.dialogs.prompts import NumberPrompt, PromptOptions
from botbuilder.core import (
    MemoryStorage,
    ConversationState,
    TurnContext,
    MessageFactory,
)
from botbuilder.core.adapters import TestAdapter, TestFlow
from botbuilder.dialogs import DialogSet, DialogTurnStatus


class NumberPromptTests(aiounittest.AsyncTestCase):
    def test_empty_should_fail(self):
        empty_id = ""
        self.assertRaises(TypeError, lambda: NumberPrompt(empty_id))

    async def test_number_prompt(self):
        # Create new ConversationState with MemoryStorage and register the state as middleware.
        conver_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and register the WaterfallDialog.
        dialog_state = conver_state.create_property("dialogState")

        dialogs = DialogSet(dialog_state)

        # Create and add number prompt to DialogSet.
        numberPrompt = NumberPrompt("NumberPrompt", None, "English")
        dialogs.add(numberPrompt)

        async def exec_test(turn_context: TurnContext) -> None:

            dialogContext = await dialogs.create_context(turn_context)
            results = await dialogContext.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                await dialogContext.begin_dialog(
                    "NumberPrompt",
                    PromptOptions(
                        prompt=MessageFactory.text("Enter quantity of cable")
                    ),
                )
            else:
                if results.status == DialogTurnStatus.Complete:
                    numberResult = results.result
                    await turn_context.send_activity(
                        MessageFactory.text(
                            f"You asked me for '{numberResult}' meters of cable."
                        )
                    )

            await conver_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        test_flow = TestFlow(None, adapter)

        test_flow2 = await test_flow.send("Hello")
        test_flow3 = await test_flow2.assert_reply("Enter quantity of cable")
        test_flow4 = await test_flow3.send("Give me twenty meters of cable")
        test_flow5 = await test_flow4.assert_reply(
            "You asked me for '20' meters of cable."
        )
