# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


import aiounittest
from botbuilder.core.adapters import (
                                    TestAdapter, 
                                    TestFlow
                                    )
from botbuilder.schema import ( 
                                Activity 
                                )
from botbuilder.core import (
                            ConversationState, 
                            MemoryStorage, 
                            TurnContext,
                            NullTelemetryClient
                            )
from botbuilder.dialogs import (
                                Dialog,
                                DialogSet,
                                WaterfallDialog,
                                WaterfallStepContext,
                                DialogTurnResult,
                                DialogContext,
                                DialogTurnStatus
                                )


begin_message = Activity()
begin_message.text = 'begin'
begin_message.type = 'message' 

class TelemetryWaterfallTests(aiounittest.AsyncTestCase):
    def test_none_telemetry_client(self):
        dialog = WaterfallDialog("myId")
        dialog.telemetry_client = None
        self.assertEqual(type(dialog.telemetry_client), NullTelemetryClient)

    async def no_test_execute_sequence_waterfall_steps(self):
        # Create new ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())
        
        # Create a DialogState property, DialogSet and register the WaterfallDialog.
        dialog_state = convo_state.create_property('dialogState')
        dialogs = DialogSet(dialog_state)
        async def step1(step) -> DialogTurnResult:
            print('IN STEP 1')
            await step.context.send_activity('bot responding.')
            return Dialog.end_of_turn
        
        async def step2(step) -> DialogTurnResult:
            print('IN STEP 2')
            return await step.end_dialog('ending WaterfallDialog.')

        mydialog = WaterfallDialog('test', [ step1, step2 ])
        await dialogs.add(mydialog)
        
        # Initialize TestAdapter
        async def exec_test(turn_context: TurnContext) -> None:

            dc = await dialogs.create_context(turn_context)
            results = await dc.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                await dc.begin_dialog('test')
            else:
                if results.status == DialogTurnStatus.Complete:
                    await turn_context.send_activity(results.result)
            await convo_state.save_changes(turn_context)
            
        adapt = TestAdapter(exec_test)

        tf = TestFlow(None, adapt)
        tf2 = await tf.send(begin_message)
        tf3 = await tf2.assert_reply('bot responding.')
        tf4 = await tf3.send('continue')
        tf5 = await tf4.assert_reply('ending WaterfallDialog.')
