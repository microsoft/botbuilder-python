# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.core import BotAdapter
from botbuilder.dialogs import DialogSet
from botbuilder.core import MemoryStorage, ConversationState
from botbuilder.core.state_property_accessor import StatePropertyAccessor


class PromptValidatorContextTests(aiounittest.AsyncTestCase):
    async def test_prompt_validator_context_end(self):
        storage = MemoryStorage()
        conv = ConversationState(storage)
        accessor = conv.create_property("dialogstate")
        ds = DialogSet(accessor)
        self.assertNotEqual(ds, None)
        # TODO: Add TestFlow

    def test_prompt_validator_context_retry_end(self):
        storage = MemoryStorage()
        conv = ConversationState(storage)
        accessor = conv.create_property("dialogstate")
        ds = DialogSet(accessor)
        self.assertNotEqual(ds, None)
        # TODO: Add TestFlow

    # All require Testflow!
