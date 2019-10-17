# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest

from botbuilder.core import MemoryStorage, TurnContext, PrivateConversationState
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import Activity, ChannelAccount, ConversationAccount

RECEIVED_MESSAGE = Activity(
    text="received",
    type="message",
    channel_id="test",
    conversation=ConversationAccount(id="convo"),
    from_property=ChannelAccount(id="user"),
)


class TestPrivateConversationState(aiounittest.AsyncTestCase):
    async def test_should_load_and_save_state_from_storage(self):
        storage = MemoryStorage()
        adapter = TestAdapter()
        context = TurnContext(adapter, RECEIVED_MESSAGE)
        private_conversation_state = PrivateConversationState(storage)

        # Simulate a "Turn" in a conversation by loading the state,
        # changing it and then saving the changes to state.
        await private_conversation_state.load(context)
        key = private_conversation_state.get_storage_key(context)
        state = private_conversation_state.get(context)
        assert state == {}, "State not loaded"
        assert key, "Key not found"
        state["test"] = "foo"
        await private_conversation_state.save_changes(context)

        # Check the storage to see if the changes to state were saved.
        items = await storage.read([key])
        assert key in items, "Saved state not found in storage."
        assert items[key]["test"] == "foo", "Missing test value in stored state."
