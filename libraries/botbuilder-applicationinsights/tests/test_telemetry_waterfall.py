# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from unittest.mock import patch
from typing import Dict
import aiounittest
from botbuilder.core.adapters import TestAdapter, TestFlow
from botbuilder.schema import Activity
from botbuilder.core import (
    ConversationState,
    MemoryStorage,
    TurnContext,
    NullTelemetryClient,
)
from botbuilder.dialogs import (
    Dialog,
    DialogSet,
    WaterfallDialog,
    DialogTurnResult,
    DialogTurnStatus,
)

BEGIN_MESSAGE = Activity()
BEGIN_MESSAGE.text = "begin"
BEGIN_MESSAGE.type = "message"


class TelemetryWaterfallTests(aiounittest.AsyncTestCase):
    def test_none_telemetry_client(self):
        # arrange
        dialog = WaterfallDialog("myId")
        # act
        dialog.telemetry_client = None
        # assert
        self.assertEqual(type(dialog.telemetry_client), NullTelemetryClient)

    @patch("botbuilder.applicationinsights.ApplicationInsightsTelemetryClient")
    async def test_execute_sequence_waterfall_steps(  # pylint: disable=invalid-name
        self, MockTelemetry
    ):
        # arrange

        # Create new ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())
        telemetry = MockTelemetry()

        # Create a DialogState property, DialogSet and register the WaterfallDialog.
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        async def step1(step) -> DialogTurnResult:
            await step.context.send_activity("bot responding.")
            return Dialog.end_of_turn

        async def step2(step) -> DialogTurnResult:
            await step.context.send_activity("ending WaterfallDialog.")
            return Dialog.end_of_turn

        # act

        my_dialog = WaterfallDialog("test", [step1, step2])
        my_dialog.telemetry_client = telemetry
        dialogs.add(my_dialog)

        # Initialize TestAdapter
        async def exec_test(turn_context: TurnContext) -> None:

            dialog_context = await dialogs.create_context(turn_context)
            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                await dialog_context.begin_dialog("test")
            else:
                if results.status == DialogTurnStatus.Complete:
                    await turn_context.send_activity(results.result)

            await convo_state.save_changes(turn_context)

        adapt = TestAdapter(exec_test)

        test_flow = TestFlow(None, adapt)
        tf2 = await test_flow.send(BEGIN_MESSAGE)
        tf3 = await tf2.assert_reply("bot responding.")
        tf4 = await tf3.send("continue")
        await tf4.assert_reply("ending WaterfallDialog.")

        # assert

        telemetry_calls = [
            ("WaterfallStart", {"DialogId": "test"}),
            ("WaterfallStep", {"DialogId": "test", "StepName": "Step1of2"}),
            ("WaterfallStep", {"DialogId": "test", "StepName": "Step2of2"}),
        ]
        self.assert_telemetry_calls(telemetry, telemetry_calls)

    @patch("botbuilder.applicationinsights.ApplicationInsightsTelemetryClient")
    async def test_ensure_end_dialog_called(
        self, MockTelemetry
    ):  # pylint: disable=invalid-name
        # arrange

        # Create new ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())
        telemetry = MockTelemetry()

        # Create a DialogState property, DialogSet and register the WaterfallDialog.
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        async def step1(step) -> DialogTurnResult:
            await step.context.send_activity("step1 response")
            return Dialog.end_of_turn

        async def step2(step) -> DialogTurnResult:
            await step.context.send_activity("step2 response")
            return Dialog.end_of_turn

        # act

        my_dialog = WaterfallDialog("test", [step1, step2])
        my_dialog.telemetry_client = telemetry
        dialogs.add(my_dialog)

        # Initialize TestAdapter
        async def exec_test(turn_context: TurnContext) -> None:

            dialog_context = await dialogs.create_context(turn_context)
            await dialog_context.continue_dialog()
            if not turn_context.responded:
                await dialog_context.begin_dialog("test", None)
            await convo_state.save_changes(turn_context)

        adapt = TestAdapter(exec_test)

        test_flow = TestFlow(None, adapt)
        tf2 = await test_flow.send(BEGIN_MESSAGE)
        tf3 = await tf2.assert_reply("step1 response")
        tf4 = await tf3.send("continue")
        tf5 = await tf4.assert_reply("step2 response")
        await tf5.send(
            "Should hit end of steps - this will restart the dialog and trigger COMPLETE event"
        )
        # assert
        telemetry_calls = [
            ("WaterfallStart", {"DialogId": "test"}),
            ("WaterfallStep", {"DialogId": "test", "StepName": "Step1of2"}),
            ("WaterfallStep", {"DialogId": "test", "StepName": "Step2of2"}),
            ("WaterfallComplete", {"DialogId": "test"}),
            ("WaterfallStart", {"DialogId": "test"}),
            ("WaterfallStep", {"DialogId": "test", "StepName": "Step1of2"}),
        ]
        print(str(telemetry.track_event.call_args_list))
        self.assert_telemetry_calls(telemetry, telemetry_calls)

    def assert_telemetry_call(
        self, telemetry_mock, index: int, event_name: str, props: Dict[str, str]
    ) -> None:
        # pylint: disable=unused-variable
        args, kwargs = telemetry_mock.track_event.call_args_list[index]
        self.assertEqual(args[0], event_name)

        for key, val in props.items():
            self.assertTrue(
                key in args[1],
                msg=f"Could not find value {key} in {args[1]} for index {index}",
            )
            self.assertTrue(isinstance(args[1], dict))
            self.assertTrue(val == args[1][key])

    def assert_telemetry_calls(self, telemetry_mock, calls) -> None:
        index = 0
        for event_name, props in calls:
            self.assert_telemetry_call(telemetry_mock, index, event_name, props)
            index += 1
        if index != len(telemetry_mock.track_event.call_args_list):
            self.assertTrue(  # pylint: disable=redundant-unittest-assert
                False,
                f"Found {len(telemetry_mock.track_event.call_args_list)} calls, testing for {index + 1}",
            )
