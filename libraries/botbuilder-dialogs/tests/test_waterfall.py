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
                            TurnContext
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

class MyWaterfallDialog(WaterfallDialog):    
    def __init__(self, id: str):
        super(MyWaterfallDialog, self).__init__(id)
        async def Waterfall2_Step1(step_context: WaterfallStepContext) -> DialogTurnResult:
            await step_context.context.send_activity("step1")
            return Dialog.end_of_turn
        
        async def Waterfall2_Step2(step_context: WaterfallStepContext) -> DialogTurnResult:
            await step_context.context.send_activity("step2")
            return Dialog.end_of_turn
         
        async def Waterfall2_Step3(step_context: WaterfallStepContext) -> DialogTurnResult:
            await step_context.context.send_activity("step3")
            return Dialog.end_of_turn
        
        self.add_step(Waterfall2_Step1)
        self.add_step(Waterfall2_Step2)
        self.add_step(Waterfall2_Step3)

begin_message = Activity()
begin_message.text = 'begin'
begin_message.type = 'message' 

class WaterfallTests(aiounittest.AsyncTestCase):
    
    def test_waterfall_none_name(self):
        self.assertRaises(TypeError, (lambda:WaterfallDialog(None)))
    
    def test_watterfall_add_none_step(self):
        waterfall = WaterfallDialog("test")
        self.assertRaises(TypeError, (lambda:waterfall.add_step(None)))
    async def test_waterfall_with_set_instead_of_array(self):
        self.assertRaises(TypeError, lambda:WaterfallDialog('a', { 1, 2 }))


    # TODO:WORK IN PROGRESS        
    async def test_execute_sequence_waterfall_steps(self):
        # Create new ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())
        
        # Create a DialogState property, DialogSet and register the WaterfallDialog.
        dialog_state = convo_state.create_property('dialogState')
        dialogs = DialogSet(dialog_state)
        async def step1(step) -> DialogTurnResult:
            await step.context.send_activity('bot responding.')
            return Dialog.end_of_turn
        
        async def step2(step) -> DialogTurnResult:
            return await step.end_dialog('ending WaterfallDialog.')

        mydialog = WaterfallDialog('test', [ step1, step2 ])
        dialogs.add(mydialog)
        
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
        
    async def test_waterfall_callback(self):
        convo_state = ConversationState(MemoryStorage())
        adapter = TestAdapter()
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)
        async def step_callback1(step: WaterfallStepContext) -> DialogTurnResult:
            await step.context.send_activity("step1")
        async def step_callback2(step: WaterfallStepContext) -> DialogTurnResult:
            await step.context.send_activity("step2")
        async def step_callback3(step: WaterfallStepContext) -> DialogTurnResult:
            await step.context.send_activity("step3")
      
        steps = [step_callback1, step_callback2, step_callback3]
        dialogs.add(WaterfallDialog("test", steps))
        self.assertNotEqual(dialogs, None)
        self.assertEqual(len(dialogs._dialogs), 1)
    
        # TODO: Fix TestFlow
    

    async def test_waterfall_with_class(self):
        convo_state = ConversationState(MemoryStorage())
        adapter = TestAdapter()
        # TODO: Fix Autosave Middleware
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)
        
        dialogs.add(MyWaterfallDialog("test"))
        self.assertNotEqual(dialogs, None)
        self.assertEqual(len(dialogs._dialogs), 1)
        
        # TODO: Fix TestFlow
        
    def test_waterfall_prompt(self):
        convo_state = ConversationState(MemoryStorage())
        adapter = TestAdapter()
        # TODO: Fix Autosave Middleware
        # TODO: Fix TestFlow
        
    def test_waterfall_nested(self):
        convo_state = ConversationState(MemoryStorage())
        adapter = TestAdapter()
        # TODO: Fix Autosave Middleware
        # TODO: Fix TestFlow
        
    def test_datetimeprompt_first_invalid_then_valid_input(self):
        convo_state = ConversationState(MemoryStorage())
        adapter = TestAdapter()
        # TODO: Fix Autosave Middleware
        # TODO: Fix TestFlow
        


        
        

