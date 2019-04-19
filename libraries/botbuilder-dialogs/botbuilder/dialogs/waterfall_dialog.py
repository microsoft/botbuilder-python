# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


import uuid
from typing import Dict
from .dialog_reason import DialogReason
from .dialog import Dialog
from .dialog_turn_result import DialogTurnResult
from .dialog_context import DialogContext
from .dialog_instance import DialogInstance
from .waterfall_step_context import WaterfallStepContext
from botbuilder.core import TurnContext
from typing import Coroutine, List


class WaterfallDialog(Dialog):
    PersistedOptions = "options"
    StepIndex = "stepIndex"
    PersistedValues = "values"
    PersistedInstanceId = "instanceId"
    
    def __init__(self, dialog_id: str, steps: [Coroutine] = None):
        super(WaterfallDialog, self).__init__(dialog_id)
        if not steps:
            self._steps = []
        else:
            self._steps = steps

    # TODO: Add WaterfallStep class
    def add_step(self, step):
        """Adds a new step to the waterfall.
        Parameters
        ----------
        step
            Step to add
           
        Returns
        -------
        WaterfallDialog
            Waterfall dialog for fluent calls to `add_step()`.
        """
        if not step:
            raise TypeError('WaterfallDialog.add_step(): step cannot be None.')
    
    async def begin_dialog(self, dc: DialogContext, options: object = None) -> DialogTurnResult:
        
        if not dc:
            raise TypeError('WaterfallDialog.begin_dialog(): dc cannot be None.')
        
        # Initialize waterfall state
        state = dc.active_dialog.state
        
        instance_id = uuid.uuid1().__str__()
        state[self.PersistedOptions] = options
        state[self.PersistedValues] = {}
        state[self.PersistedInstanceId] = instance_id
        
        properties = {}
        properties['dialog_id'] = id
        properties['instance_id'] = instance_id
        
        # Run first stepkinds
        return await self.run_step(dc, 0, DialogReason.BeginCalled, None) 
    
    async def continue_dialog(self, dc: DialogContext, reason: DialogReason, result: object) -> DialogTurnResult:
        if not dc:
            raise TypeError('WaterfallDialog.continue_dialog(): dc cannot be None.')
        
        if dc.context.activity.type != ActivityTypes.message:
            return Dialog.end_of_turn
        
        return await self.resume_dialog(dc, DialogReason.ContinueCalled, dc.context.activity.text)
    
    async def resume_dialog(self, dc: DialogContext, reason: DialogReason, result: object):
        if not dc:
            raise TypeError('WaterfallDialog.resume_dialog(): dc cannot be None.')
        
        # Increment step index and run step
        state = dc.active_dialog.state
        
        # Future Me: 
        # If issues with CosmosDB, see https://github.com/Microsoft/botbuilder-dotnet/issues/871
        # for hints.
        return self.run_step(dc, state[StepIndex] + 1, reason, result)
    
    async def end_dialog(self, turn_context: TurnContext, instance: DialogInstance, reason: DialogReason):
        # TODO: Add telemetry logging
        return 
    
    async def on_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # TODO: Add telemetry logging
        return await self._steps[step_context.index](step_context)
    
    async def run_step(self, dc: DialogContext, index: int, reason: DialogReason, result: object) -> DialogTurnResult:
        if not dc:
            raise TypeError('WaterfallDialog.run_steps(): dc cannot be None.')
        if index < len(self._steps):
            # Update persisted step index
            state = dc.active_dialog.state
            state[self.StepIndex] = index
            
            # Create step context
            options = state[self.PersistedOptions]
            values = state[self.PersistedValues]
            step_context = WaterfallStepContext(self, dc, options, values, index, reason, result)
            return await self.on_step(step_context)
        else:
            # End of waterfall so just return any result to parent
            return dc.end_dialog(result)
