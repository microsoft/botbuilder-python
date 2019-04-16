# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


import unittest
from botbuilder.core import BotAdapter
from botbuilder.dialogs import DialogSet


class DialogSetTests(unittest.TestCase):
    def DialogSet_ConstructorValid():
        storage = MemoryStorage();
        convoState = ConversationState(storage);
        dialogStateProperty = convoState.create_property("dialogstate");
        ds = DialogSet(dialogStateProperty);
    
    def DialogSet_ConstructorNullProperty():
        ds = DialogSet(null);

