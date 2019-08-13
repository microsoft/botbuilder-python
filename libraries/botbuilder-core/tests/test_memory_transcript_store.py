# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# pylint: disable=missing-docstring, unused-import
import sys
import copy
import uuid
import datetime
from typing import Awaitable, Callable, Dict, List
from unittest.mock import patch, Mock
import aiounittest

from botbuilder.core import (
    AnonymousReceiveMiddleware,
    BotTelemetryClient,
    MemoryTranscriptStore,
    MiddlewareSet,
    Middleware,
    TurnContext,
)
from botbuilder.core.adapters import TestAdapter, TestFlow
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    ConversationAccount,
    ConversationReference,
)

# pylint: disable=line-too-long,missing-docstring
class TestMemoryTranscriptStore(aiounittest.AsyncTestCase):
    # pylint: disable=unused-argument
    async def test_null_transcript_store(self):
        memory_transcript = MemoryTranscriptStore()
        with self.assertRaises(TypeError):
            await memory_transcript.log_activity(None)

    async def test_log_activity(self):
        memory_transcript = MemoryTranscriptStore()
        conversation_id = "_log_activity"
        date = datetime.datetime.now()
        activity = self.create_activities(conversation_id, date, 1)[-1]
        await memory_transcript.log_activity(activity)

    async def test_get_activity_none(self):
        memory_transcript = MemoryTranscriptStore()
        conversation_id = "_log_activity"
        await memory_transcript.get_transcript_activities("test", conversation_id)

    async def test_get_single_activity(self):
        memory_transcript = MemoryTranscriptStore()
        conversation_id = "_log_activity"
        date = datetime.datetime.now()
        activity = self.create_activities(conversation_id, date, count=1)[-1]
        await memory_transcript.log_activity(activity)
        result = await memory_transcript.get_transcript_activities(
            "test", conversation_id
        )
        self.assertNotEqual(result.items, None)
        self.assertEqual(result.items[0].text, "0")

    async def test_get_multiple_activity(self):
        memory_transcript = MemoryTranscriptStore()
        conversation_id = "_log_activity"
        date = datetime.datetime.now()
        activities = self.create_activities(conversation_id, date, count=10)
        for activity in activities:
            await memory_transcript.log_activity(activity)
        result = await memory_transcript.get_transcript_activities(
            "test", conversation_id
        )
        self.assertNotEqual(result.items, None)
        self.assertEqual(len(result.items), 20)  # 2 events logged each iteration

    async def test_delete_transcript(self):
        memory_transcript = MemoryTranscriptStore()
        conversation_id = "_log_activity"
        date = datetime.datetime.now()
        activity = self.create_activities(conversation_id, date, count=1)[-1]
        await memory_transcript.log_activity(activity)
        result = await memory_transcript.get_transcript_activities(
            "test", conversation_id
        )
        self.assertNotEqual(result.items, None)
        await memory_transcript.delete_transcript("test", conversation_id)
        result = await memory_transcript.get_transcript_activities(
            "test", conversation_id
        )
        self.assertEqual(result.items, None)

    def create_activities(self, conversation_id: str, date: datetime, count: int = 5):
        activities: List[Activity] = []
        time_stamp = date
        for i in range(count):
            activities.append(
                Activity(
                    type=ActivityTypes.message,
                    timestamp=time_stamp,
                    id=str(uuid.uuid4()),
                    text=str(i),
                    channel_id="test",
                    from_property=ChannelAccount(id=f"User{i}"),
                    conversation=ConversationAccount(id=conversation_id),
                    recipient=ChannelAccount(id="bot1", name="2"),
                    service_url="http://foo.com/api/messages",
                )
            )
            time_stamp = time_stamp + datetime.timedelta(0, 60)
            activities.append(
                Activity(
                    type=ActivityTypes.message,
                    timestamp=date,
                    id=str(uuid.uuid4()),
                    text=str(i),
                    channel_id="test",
                    from_property=ChannelAccount(id="Bot1", name="2"),
                    conversation=ConversationAccount(id=conversation_id),
                    recipient=ChannelAccount(id=f"User{i}"),
                    service_url="http://foo.com/api/messages",
                )
            )
            time_stamp = time_stamp + datetime.timedelta(
                0, 60
            )  # days, seconds, then other fields.
        return activities
