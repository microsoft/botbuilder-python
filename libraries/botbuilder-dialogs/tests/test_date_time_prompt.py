# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.dialogs.prompts import DateTimePrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.core import ConversationState, MemoryStorage, TurnContext
from botbuilder.dialogs import DialogSet, DialogTurnStatus
from botbuilder.core.adapters import TestAdapter, TestFlow


class DatetimePromptTests(aiounittest.AsyncTestCase):
    async def test_date_time_prompt(self):
        # Create new ConversationState with MemoryStorage and register the state as middleware.
        conver_state = ConversationState(MemoryStorage())

        # Create a DialogState property
        dialog_state = conver_state.create_property("dialogState")

        # Create new DialogSet.
        dialogs = DialogSet(dialog_state)

        # Create and add DateTime prompt to DialogSet.
        date_time_prompt = DateTimePrompt("DateTimePrompt")

        dialogs.add(date_time_prompt)

        # Initialize TestAdapter
        async def exec_test(turn_context: TurnContext) -> None:
            prompt_msg = "What date would you like?"
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:

                options = PromptOptions(prompt=MessageFactory.text(prompt_msg))
                await dialog_context.begin_dialog("DateTimePrompt", options)
            else:
                if results.status == DialogTurnStatus.Complete:
                    resolution = results.result[0]
                    reply = MessageFactory.text(
                        f"Timex: '{resolution.timex}' Value: '{resolution.value}'"
                    )
                    await turn_context.send_activity(reply)
            await conver_state.save_changes(turn_context)

        adapt = TestAdapter(exec_test)

        test_flow = TestFlow(None, adapt)
        tf2 = await test_flow.send("hello")
        tf3 = await tf2.assert_reply("What date would you like?")
        tf4 = await tf3.send("5th December 2018 at 9am")
        await tf4.assert_reply("Timex: '2018-12-05T09' Value: '2018-12-05 09:00:00'")
