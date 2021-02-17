# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.dialogs import DialogSet, ComponentDialog, WaterfallDialog
from botbuilder.core import ConversationState, MemoryStorage, NullTelemetryClient


class MyBotTelemetryClient(NullTelemetryClient):
    # pylint: disable=useless-return
    def __init__(self):
        super().__init__()
        return


class DialogSetTests(aiounittest.AsyncTestCase):
    def test_dialogset_constructor_valid(self):
        convo_state = ConversationState(MemoryStorage())
        dialog_state_property = convo_state.create_property("dialogstate")
        dialog_set = DialogSet(dialog_state_property)
        assert dialog_set is not None

    def test_dialogset_constructor_null_property(self):
        self.assertRaises(TypeError, lambda: DialogSet(None))

    def test_dialogset_constructor_null_from_componentdialog(self):
        ComponentDialog("MyId")

    def test_dialogset_telemetryset(self):
        convo_state = ConversationState(MemoryStorage())
        dialog_state_property = convo_state.create_property("dialogstate")
        dialog_set = DialogSet(dialog_state_property)

        dialog_set.add(WaterfallDialog("A"))
        dialog_set.add(WaterfallDialog("B"))

        self.assertTrue(
            isinstance(
                dialog_set.find_dialog("A").telemetry_client, NullTelemetryClient
            )
        )
        self.assertTrue(
            isinstance(
                dialog_set.find_dialog("B").telemetry_client, NullTelemetryClient
            )
        )

        dialog_set.telemetry_client = MyBotTelemetryClient()

        self.assertTrue(
            isinstance(
                dialog_set.find_dialog("A").telemetry_client, MyBotTelemetryClient
            )
        )
        self.assertTrue(
            isinstance(
                dialog_set.find_dialog("B").telemetry_client, MyBotTelemetryClient
            )
        )

    def test_dialogset_nulltelemetryset(self):
        convo_state = ConversationState(MemoryStorage())
        dialog_state_property = convo_state.create_property("dialogstate")
        dialog_set = DialogSet(dialog_state_property)

        dialog_set.add(WaterfallDialog("A"))
        dialog_set.add(WaterfallDialog("B"))

        dialog_set.telemetry_client = MyBotTelemetryClient()
        dialog_set.telemetry_client = None

        self.assertFalse(
            isinstance(
                dialog_set.find_dialog("A").telemetry_client, MyBotTelemetryClient
            )
        )
        self.assertFalse(
            isinstance(
                dialog_set.find_dialog("B").telemetry_client, MyBotTelemetryClient
            )
        )
        self.assertTrue(
            isinstance(
                dialog_set.find_dialog("A").telemetry_client, NullTelemetryClient
            )
        )
        self.assertTrue(
            isinstance(
                dialog_set.find_dialog("B").telemetry_client, NullTelemetryClient
            )
        )

    # pylint: disable=pointless-string-statement
    """
    This test will be enabled when telematry tests are fixed for DialogSet telemetry
    def test_dialogset_addtelemetryset(self):
        convo_state = ConversationState(MemoryStorage())
        dialog_state_property = convo_state.create_property("dialogstate")
        dialog_set = DialogSet(dialog_state_property)

        dialog_set.add(WaterfallDialog("A"))
        dialog_set.add(WaterfallDialog("B"))

        dialog_set.telemetry_client = MyBotTelemetryClient()

        dialog_set.add(WaterfallDialog("C"))

        self.assertTrue(isinstance(dialog_set.find_dialog("C").telemetry_client, MyBotTelemetryClient))
    """
