# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from __future__ import annotations # For PEP563
import uuid
from typing import Dict
from .dialog_reason import DialogReason
from .dialog import Dialog
from botbuilder.dialogs.dialog_turn_result import DialogTurnResult

class WaterfallDialog(Dialog):
    PersistedOptions = "options"
    StepIndex = "stepIndex"
    PersistedValues = "values"
    PersistedInstanceId = "instanceId"
    
    def __init__(self, dialog_id: str, steps: [] = None):
        super(WaterfallDialog, self).__init__(dialog_id)
        if not steps:
            self._steps = []
        else:
            self._steps = steps

    # TODO: Add WaterfallStep class
    def add_step(self, step) -> WaterfallDialog:
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
        state[PersistedOptions] = options
        state[PersistedValues] = Dict[str, object]
        state[PersistedInstanceId] = instanceId
        
        properties = Dict[str, object]
        properties['dialog_id'] = id
        properties['instance_id'] = instance_id
        
        # Run first stepkinds
        return await run_step(dc, 0, DialogReason.BeginCalled, None) 
    
    async def continue_dialog(self, dc: DialogContext, reason: DialogReason, result: Object) -> DialogTurnResult:
        if not dc:
            raise TypeError('WaterfallDialog.continue_dialog(): dc cannot be None.')
        
        if dc.context.activity.type != ActivityTypes.message:
            return Dialog.end_of_turn
        
        return await resume_dialog(dc, DialogReason.ContinueCalled, dc.context.activity.text)
    
    async def resume_dialog(self, dc: DialogContext, reason: DialogReason, result: object):
        if not dc:
            raise TypeError('WaterfallDialog.resume_dialog(): dc cannot be None.')
        
        # Increment step index and run step
        state = dc.active_dialog.state
        
        # Future Me: 
        # If issues with CosmosDB, see https://github.com/Microsoft/botbuilder-dotnet/issues/871
        # for hints.
        return run_step(dc, state[StepIndex] + 1, reason, result)
    
    async def end_dialog(self, turn_context: TurnContext, instance: DialogInstance, reason: DialogReason):
        # TODO: Add telemetry logging
        return 
    
    async def on_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # TODO: Add telemetry logging
        return await self._steps[step_context.index](step_context)
    
    async def run_steps(self, dc: DialogContext, index: int, reason: DialogReason, result: Object) -> DialogTurnResult:
        if not dc:
            raise TypeError('WaterfallDialog.run_steps(): dc cannot be None.')
        if index < _steps.size:
            # Update persisted step index
            state = dc.active_dialog.state
            state[StepIndex] = index
            
            # Create step context
            options = state[PersistedOptions]
            values = state[PersistedValues]
            step_context = WaterfallStepContext(self, dc, options, values, index, reason, result)
            return await on_step(step_context)
        else:
            # End of waterfall so just return any result to parent
            return dc.end_dialog(result)
