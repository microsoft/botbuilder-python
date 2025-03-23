# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.dialogs import (
    DialogDependencies,
    DialogSet,
    ComponentDialog,
    WaterfallDialog,
)
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

    def test_dialogset_raises_on_repeated_id(self):
        convo_state = ConversationState(MemoryStorage())
        dialog_state_property = convo_state.create_property("dialogstate")
        dialog_set = DialogSet(dialog_state_property)

        dialog_set.add(WaterfallDialog("A"))
        with self.assertRaises(TypeError):
            dialog_set.add(WaterfallDialog("A"))

        self.assertTrue(dialog_set.find_dialog("A") is not None)

    def test_dialogset_idempotenticy_add(self):
        convo_state = ConversationState(MemoryStorage())
        dialog_state_property = convo_state.create_property("dialogstate")
        dialog_set = DialogSet(dialog_state_property)
        dialog_a = WaterfallDialog("A")
        dialog_set.add(dialog_a)
        dialog_set.add(dialog_a)

    async def test_dialogset_dependency_tree_add(self):
        class MyDialog(WaterfallDialog, DialogDependencies):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._dependencies = []

            def add_dependency(self, dialog):
                self._dependencies.append(dialog)

            def get_dependencies(self):
                return self._dependencies

        convo_state = ConversationState(MemoryStorage())
        dialog_state_property = convo_state.create_property("dialogstate")
        dialog_set = DialogSet(dialog_state_property)

        dialog_a = MyDialog("A")
        dialog_b = MyDialog("B")
        dialog_c = MyDialog("C")
        dialog_d = MyDialog("D")
        dialog_e = MyDialog("E")
        dialog_i = MyDialog("I")

        dialog_a.add_dependency(dialog_b)

        # Multi-hierarchy should be OK
        dialog_b.add_dependency(dialog_d)
        dialog_b.add_dependency(dialog_e)

        # circular dependencies should be OK
        dialog_c.add_dependency(dialog_d)
        dialog_d.add_dependency(dialog_c)

        assert dialog_set.find_dialog(dialog_a.id) is None
        dialog_set.add(dialog_a)

        for dialog in [
            dialog_a,
            dialog_b,
            dialog_c,
            dialog_d,
            dialog_e,
        ]:
            self.assertTrue(dialog_set.find_dialog(dialog.id) is dialog)
            self.assertTrue(await dialog_set.find(dialog.id) is dialog)

        assert dialog_set.find_dialog(dialog_i.id) is None

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
