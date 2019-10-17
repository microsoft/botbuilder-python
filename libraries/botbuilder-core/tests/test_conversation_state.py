# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest

from botbuilder.core import TurnContext, MemoryStorage, ConversationState
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import Activity, ConversationAccount

RECEIVED_MESSAGE = Activity(
    type="message",
    text="received",
    channel_id="test",
    conversation=ConversationAccount(id="convo"),
)
MISSING_CHANNEL_ID = Activity(
    type="message", text="received", conversation=ConversationAccount(id="convo")
)
MISSING_CONVERSATION = Activity(type="message", text="received", channel_id="test")
END_OF_CONVERSATION = Activity(
    type="endOfConversation",
    channel_id="test",
    conversation=ConversationAccount(id="convo"),
)


class TestConversationState(aiounittest.AsyncTestCase):
    storage = MemoryStorage()
    adapter = TestAdapter()
    context = TurnContext(adapter, RECEIVED_MESSAGE)
    middleware = ConversationState(storage)

    async def test_should_reject_with_error_if_channel_id_is_missing(self):
        context = TurnContext(self.adapter, MISSING_CHANNEL_ID)

        async def next_middleware():
            assert False, "should not have called next_middleware"

        try:
            await self.middleware.on_process_request(context, next_middleware)
        except AttributeError:
            pass
        except Exception as error:
            raise error
        else:
            raise AssertionError(
                "Should not have completed and not raised AttributeError."
            )

    async def test_should_reject_with_error_if_conversation_is_missing(self):
        context = TurnContext(self.adapter, MISSING_CONVERSATION)

        async def next_middleware():
            assert False, "should not have called next_middleware"

        try:
            await self.middleware.on_process_request(context, next_middleware)
        except AttributeError:
            pass
        except Exception as error:
            raise error
        else:
            raise AssertionError(
                "Should not have completed and not raised AttributeError."
            )
