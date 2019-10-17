# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.dialogs import DialogSet
from botbuilder.core import MemoryStorage, ConversationState


class PromptValidatorContextTests(aiounittest.AsyncTestCase):
    async def test_prompt_validator_context_end(self):
        storage = MemoryStorage()
        conv = ConversationState(storage)
        accessor = conv.create_property("dialogstate")
        dialog_set = DialogSet(accessor)
        self.assertNotEqual(dialog_set, None)
        # TODO: Add TestFlow

    def test_prompt_validator_context_retry_end(self):
        storage = MemoryStorage()
        conv = ConversationState(storage)
        accessor = conv.create_property("dialogstate")
        dialog_set = DialogSet(accessor)
        self.assertNotEqual(dialog_set, None)
        # TODO: Add TestFlow

    # All require Testflow!
