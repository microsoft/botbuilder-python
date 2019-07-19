# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.dialogs import DialogSet, ComponentDialog
from botbuilder.core import ConversationState, MemoryStorage


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
