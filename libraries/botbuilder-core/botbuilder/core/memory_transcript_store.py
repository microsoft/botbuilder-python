# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""The memory transcript store stores transcripts in volatile memory."""
import datetime
from typing import List, Dict
from botbuilder.schema import Activity
from .transcript_logger import PagedResult, TranscriptInfo, TranscriptStore


# pylint: disable=line-too-long
class MemoryTranscriptStore(TranscriptStore):
    """This provider is most useful for simulating production storage when running locally against the
    emulator or as part of a unit test.
    """

    channels: Dict[str, Dict[str, Activity]] = {}

    async def log_activity(self, activity: Activity) -> None:
        if not activity:
            raise TypeError("activity cannot be None for log_activity()")

        # get channel
        channel = {}
        if not activity.channel_id in self.channels:
            channel = {}
            self.channels[activity.channel_id] = channel
        else:
            channel = self.channels[activity.channel_id]

        # Get conversation transcript.
        transcript = []
        if activity.conversation.id in channel:
            transcript = channel[activity.conversation.id]
        else:
            transcript = []
            channel[activity.conversation.id] = transcript

        transcript.append(activity)

    async def get_transcript_activities(
        self,
        channel_id: str,
        conversation_id: str,
        continuation_token: str = None,
        start_date: datetime = datetime.datetime.min,
    ) -> "PagedResult[Activity]":
        if not channel_id:
            raise TypeError("Missing channel_id")

        if not conversation_id:
            raise TypeError("Missing conversation_id")

        paged_result = PagedResult()
        if channel_id in self.channels:
            channel = self.channels[channel_id]
            if conversation_id in channel:
                transcript = channel[conversation_id]
                if continuation_token:
                    paged_result.items = (
                        [
                            x
                            for x in sorted(
                                transcript,
                                key=lambda x: x.timestamp or str(datetime.datetime.min),
                                reverse=False,
                            )
                            if x.timestamp >= start_date
                        ]
                        .dropwhile(lambda x: x.id != continuation_token)
                        .Skip(1)[:20]
                    )
                    if paged_result.items.count == 20:
                        paged_result.continuation_token = paged_result.items[-1].id
                else:
                    paged_result.items = [
                        x
                        for x in sorted(
                            transcript,
                            key=lambda x: x.timestamp or datetime.datetime.min,
                            reverse=False,
                        )
                        if (x.timestamp or datetime.datetime.min) >= start_date
                    ][:20]
                    if paged_result.items.count == 20:
                        paged_result.continuation_token = paged_result.items[-1].id

        return paged_result

    async def delete_transcript(self, channel_id: str, conversation_id: str) -> None:
        if not channel_id:
            raise TypeError("channel_id should not be None")

        if not conversation_id:
            raise TypeError("conversation_id should not be None")

        if channel_id in self.channels:
            if conversation_id in self.channels[channel_id]:
                del self.channels[channel_id][conversation_id]

    async def list_transcripts(
        self, channel_id: str, continuation_token: str = None
    ) -> "PagedResult[TranscriptInfo]":
        if not channel_id:
            raise TypeError("Missing channel_id")

        paged_result = PagedResult()

        if channel_id in self.channels:
            channel: Dict[str, List[Activity]] = self.channels[channel_id]

            if continuation_token:
                paged_result.items = (
                    sorted(
                        [
                            TranscriptInfo(
                                channel_id,
                                c.value()[0].timestamp if c.value() else None,
                                c.id,
                            )
                            for c in channel
                        ],
                        key=lambda x: x.created,
                        reverse=True,
                    )
                    .dropwhile(lambda x: x.id != continuation_token)
                    .Skip(1)
                    .Take(20)
                )
                if paged_result.items.count == 20:
                    paged_result.continuation_token = paged_result.items[-1].id
            else:
                paged_result.items = (
                    sorted(
                        [
                            TranscriptInfo(
                                channel_id,
                                c.value()[0].timestamp if c.value() else None,
                                c.id,
                            )
                            for c in channel
                        ],
                        key=lambda x: x.created,
                        reverse=True,
                    )
                    .dropwhile(lambda x: x.id != continuation_token)
                    .Skip(1)
                    .Take(20)
                )
                if paged_result.items.count == 20:
                    paged_result.continuation_token = paged_result.items[-1].id

        return paged_result
