# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


import aiounittest
from botbuilder.core.test_adapter import TestAdapter, TestFlow
from botbuilder.core.memory_storage import MemoryStorage
from botbuilder.core.conversation_state import ConversationState
from botbuilder.dialogs.dialog_set import DialogSet
from botbuilder.dialogs.waterfall_dialog import WaterfallDialog
from botbuilder.dialogs.waterfall_step_context import WaterfallStepContext
from botbuilder.dialogs.dialog_turn_result import DialogTurnResult

async def Waterfall2_Step1(step_context: WaterfallStepContext) -> DialogTurnResult:
    await step_context.context.send_activity("step1")
    return Dialog.end_of_turn

async def Waterfall2_Step2(step_context: WaterfallStepContext) -> DialogTurnResult:
    await step_context.context.send_activity("step2")
    return Dialog.end_of_turn
 
async def Waterfall2_Step3(step_context: WaterfallStepContext) -> DialogTurnResult:
    await step_context.context.send_activity("step3")
    return Dialog.end_of_turn

class MyWaterfallDialog(WaterfallDialog):    
    def __init__(self, id: str):
        super(WaterfallDialog, self).__init__(id)
        self.add_step(Waterfall2_Step1)
        self.add_step(Waterfall2_Step2)
        self.add_step(Waterfall2_Step3)


class WaterfallTests(aiounittest.AsyncTestCase):
    def test_waterfall_none_name(self):
        self.assertRaises(TypeError, (lambda:WaterfallDialog(None)))
    
    def test_watterfall_add_none_step(self):
        waterfall = WaterfallDialog("test")
        self.assertRaises(TypeError, (lambda:waterfall.add_step(None)))
        
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
        await dialogs.add(WaterfallDialog("test", steps))
        self.assertNotEqual(dialogs, None)
        self.assertEqual(len(dialogs._dialogs), 1)
    
        # TODO: Fix TestFlow
    

    async def test_waterfall_with_class(self):
        convo_state = ConversationState(MemoryStorage())
        adapter = TestAdapter()
        # TODO: Fix Autosave Middleware
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)
        
        await dialogs.add(MyWaterfallDialog("test"))
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
        


        
        

