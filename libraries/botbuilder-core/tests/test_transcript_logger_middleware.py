# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest

from botbuilder.core import (
    MemoryTranscriptStore,
    TranscriptLoggerMiddleware,
    TurnContext,
)
from botbuilder.core.adapters import TestAdapter, TestFlow
from botbuilder.schema import Activity, ActivityEventNames, ActivityTypes


class TestTranscriptLoggerMiddleware(aiounittest.AsyncTestCase):
    async def test_should_not_log_continue_conversation(self):
        transcript_store = MemoryTranscriptStore()
        conversation_id = ""
        sut = TranscriptLoggerMiddleware(transcript_store)

        async def aux_logic(context: TurnContext):
            nonlocal conversation_id
            conversation_id = context.activity.conversation.id

        adapter = TestAdapter(aux_logic)
        adapter.use(sut)

        continue_conversation_activity = Activity(
            type=ActivityTypes.event, name=ActivityEventNames.continue_conversation
        )

        test_flow = TestFlow(None, adapter)
        step1 = await test_flow.send("foo")
        step2 = await step1.send("bar")
        await step2.send(continue_conversation_activity)

        paged_result = await transcript_store.get_transcript_activities(
            "test", conversation_id
        )
        self.assertEqual(
            len(paged_result.items),
            2,
            "only the two message activities should be logged",
        )
