# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


import uuid
from typing import Coroutine
from botbuilder.core import TurnContext
from botbuilder.schema import ActivityTypes
from .dialog_reason import DialogReason
from .dialog import Dialog
from .dialog_turn_result import DialogTurnResult
from .dialog_context import DialogContext
from .dialog_instance import DialogInstance
from .waterfall_step_context import WaterfallStepContext


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
            if not isinstance(steps, list):
                raise TypeError("WaterfallDialog(): steps must be list of steps")
            self._steps = steps

    def add_step(self, step):
        """
        Adds a new step to the waterfall.
        :param step: Step to add
        :return: Waterfall dialog for fluent calls to `add_step()`.
        """
        if not step:
            raise TypeError("WaterfallDialog.add_step(): step cannot be None.")

        self._steps.append(step)
        return self

    async def begin_dialog(
        self, dialog_context: DialogContext, options: object = None
    ) -> DialogTurnResult:
        if not dialog_context:
            raise TypeError("WaterfallDialog.begin_dialog(): dc cannot be None.")

        # Initialize waterfall state
        state = dialog_context.active_dialog.state

        instance_id = uuid.uuid1().__str__()
        state[self.PersistedOptions] = options
        state[self.PersistedValues] = {}
        state[self.PersistedInstanceId] = instance_id

        properties = {}
        properties["DialogId"] = self.id
        properties["InstanceId"] = instance_id
        self.telemetry_client.track_event("WaterfallStart", properties)

        # Run first stepkinds
        return await self.run_step(dialog_context, 0, DialogReason.BeginCalled, None)

    async def continue_dialog(  # pylint: disable=unused-argument,arguments-differ
        self,
        dialog_context: DialogContext = None,
        reason: DialogReason = None,
        result: object = NotImplementedError(),
    ) -> DialogTurnResult:
        if not dialog_context:
            raise TypeError("WaterfallDialog.continue_dialog(): dc cannot be None.")

        if dialog_context.context.activity.type != ActivityTypes.message:
            return Dialog.end_of_turn

        return await self.resume_dialog(
            dialog_context,
            DialogReason.ContinueCalled,
            dialog_context.context.activity.text,
        )

    async def resume_dialog(
        self, dialog_context: DialogContext, reason: DialogReason, result: object
    ):
        if dialog_context is None:
            raise TypeError("WaterfallDialog.resume_dialog(): dc cannot be None.")

        # Increment step index and run step
        state = dialog_context.active_dialog.state

        # Future Me:
        # If issues with CosmosDB, see https://github.com/Microsoft/botbuilder-dotnet/issues/871
        # for hints.
        return await self.run_step(
            dialog_context, state[self.StepIndex] + 1, reason, result
        )

    async def end_dialog(  # pylint: disable=unused-argument
        self, context: TurnContext, instance: DialogInstance, reason: DialogReason
    ) -> None:
        if reason is DialogReason.CancelCalled:
            index = instance.state[self.StepIndex]
            step_name = self.get_step_name(index)
            instance_id = str(instance.state[self.PersistedInstanceId])
            properties = {
                "DialogId": self.id,
                "StepName": step_name,
                "InstanceId": instance_id,
            }
            self.telemetry_client.track_event("WaterfallCancel", properties)
        else:
            if reason is DialogReason.EndCalled:
                instance_id = str(instance.state[self.PersistedInstanceId])
                properties = {"DialogId": self.id, "InstanceId": instance_id}
                self.telemetry_client.track_event("WaterfallComplete", properties)

        return

    async def on_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_name = self.get_step_name(step_context.index)
        instance_id = str(step_context.active_dialog.state[self.PersistedInstanceId])
        properties = {
            "DialogId": self.id,
            "StepName": step_name,
            "InstanceId": instance_id,
        }
        self.telemetry_client.track_event("WaterfallStep", properties)
        return await self._steps[step_context.index](step_context)

    async def run_step(
        self,
        dialog_context: DialogContext,
        index: int,
        reason: DialogReason,
        result: object,
    ) -> DialogTurnResult:
        if not dialog_context:
            raise TypeError(
                "WaterfallDialog.run_steps(): dialog_context cannot be None."
            )
        if index < len(self._steps):
            # Update persisted step index
            state = dialog_context.active_dialog.state
            state[self.StepIndex] = index

            # Create step context
            options = state[self.PersistedOptions]
            values = state[self.PersistedValues]
            step_context = WaterfallStepContext(
                self, dialog_context, options, values, index, reason, result
            )
            return await self.on_step(step_context)

        # End of waterfall so just return any result to parent
        return await dialog_context.end_dialog(result)

    def get_step_name(self, index: int) -> str:
        """
        Give the waterfall step a unique name
        """
        step_name = self._steps[index].__qualname__

        if not step_name or step_name.endswith("<lambda>"):
            step_name = f"Step{index + 1}of{len(self._steps)}"

        return step_name
