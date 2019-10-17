# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest

from botbuilder.core import TurnContext, MemoryStorage, UserState
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import Activity, ChannelAccount

RECEIVED_MESSAGE = Activity(
    type="message",
    text="received",
    channel_id="test",
    from_property=ChannelAccount(id="user"),
)
MISSING_CHANNEL_ID = Activity(
    type="message", text="received", from_property=ChannelAccount(id="user")
)
MISSING_FROM_PROPERTY = Activity(type="message", text="received", channel_id="test")


class TestUserState(aiounittest.AsyncTestCase):
    storage = MemoryStorage()
    adapter = TestAdapter()
    context = TurnContext(adapter, RECEIVED_MESSAGE)
    user_state = UserState(storage)

    async def test_should_load_and_save_state_from_storage(self):
        await self.user_state.load(self.context)
        key = self.user_state.get_storage_key(self.context)
        state = self.user_state.get(self.context)

        assert state is not None, "State not loaded"
        assert key, "Key not found"

        state["test"] = "foo"
        await self.user_state.save_changes(self.context)

        items = await self.storage.read([key])

        assert key in items, "Saved state not found in storage"
        assert items[key]["test"] == "foo", "Missing saved value in stored storage"

    async def test_should_reject_with_error_if_channel_id_is_missing(self):
        context = TurnContext(self.adapter, MISSING_CHANNEL_ID)

        async def next_middleware():
            assert False, "Should not have called next_middleware"

        try:
            await self.user_state.on_process_request(context, next_middleware)
        except AttributeError:
            pass
        else:
            raise AssertionError(
                "Should not have completed and not raised AttributeError."
            )

    async def test_should_reject_with_error_if_from_property_is_missing(self):
        context = TurnContext(self.adapter, MISSING_FROM_PROPERTY)

        async def next_middleware():
            assert False, "Should not have called next_middleware"

        try:
            await self.user_state.on_process_request(context, next_middleware)
        except AttributeError:
            pass
        else:
            raise AssertionError(
                "Should not have completed and not raised AttributeError."
            )
