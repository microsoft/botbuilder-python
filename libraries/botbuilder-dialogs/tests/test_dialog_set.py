# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


import unittest
from botbuilder.core import BotAdapter
from botbuilder.dialogs import DialogSet
from botbuilder.core import MemoryStorage, ConversationState
from botbuilder.core.state_property_accessor import StatePropertyAccessor


class DialogSetTests(unittest.TestCase):
    def test_DialogSet_ConstructorValid(self):
        storage = MemoryStorage();
        conv = ConversationState(storage)
        accessor = conv.create_property("dialogstate")
        ds = DialogSet(accessor);
        self.assertNotEqual(ds, None)
    
    def test_DialogSet_ConstructorNoneProperty(self):
        self.assertRaises(TypeError, lambda:DialogSet(None))

        
        

