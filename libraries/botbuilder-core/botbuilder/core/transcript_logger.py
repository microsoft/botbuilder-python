# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Logs incoming and outgoing activities to a TranscriptStore.."""

import datetime
import copy
import random
import string
from queue import Queue
from abc import ABC, abstractmethod
from typing import Awaitable, Callable, List
from botbuilder.schema import (
    Activity,
    ActivityEventNames,
    ActivityTypes,
    ChannelAccount,
    ConversationReference,
)
from .middleware_set import Middleware
from .turn_context import TurnContext


class TranscriptLogger(ABC):
    """Transcript logger stores activities for conversations for recall."""

    @abstractmethod
    async def log_activity(self, activity: Activity) -> None:
        """Log an activity to the transcript.
        :param activity:Activity being logged.
        """
        raise NotImplementedError


class TranscriptLoggerMiddleware(Middleware):
    """Logs incoming and outgoing activities to a TranscriptStore."""

    def __init__(self, logger: TranscriptLogger):
        if not logger:
            raise TypeError(
                "TranscriptLoggerMiddleware requires a TranscriptLogger instance."
            )
        self.logger = logger

    async def on_turn(
        self, context: TurnContext, logic: Callable[[TurnContext], Awaitable]
    ):
        """Initialization for middleware.
        :param context: Context for the current turn of conversation with the user.
        :param logic: Function to call at the end of the middleware chain.
        """
        transcript = Queue()
        activity = context.activity
        # Log incoming activity at beginning of turn
        if activity:
            if not activity.from_property:
                activity.from_property = ChannelAccount()
            if not activity.from_property.role:
                activity.from_property.role = "user"

            # We should not log ContinueConversation events used by skills to initialize the middleware.
            if not (
                context.activity.type == ActivityTypes.event
                and context.activity.name == ActivityEventNames.continue_conversation
            ):
                await self.log_activity(transcript, copy.copy(activity))

        # hook up onSend pipeline
        # pylint: disable=unused-argument
        async def send_activities_handler(
            ctx: TurnContext,
            activities: List[Activity],
            next_send: Callable[[], Awaitable[None]],
        ):
            # Run full pipeline
            responses = await next_send()
            for index, activity in enumerate(activities):
                cloned_activity = copy.copy(activity)
                if responses and index < len(responses):
                    cloned_activity.id = responses[index].id

                # For certain channels, a ResourceResponse with an id is not always sent to the bot.
                # This fix uses the timestamp on the activity to populate its id for logging the transcript
                # If there is no outgoing timestamp, the current time for the bot is used for the activity.id
                if not cloned_activity.id:
                    alphanumeric = string.ascii_lowercase + string.digits
                    prefix = "g_" + "".join(
                        random.choice(alphanumeric) for i in range(5)
                    )
                    epoch = datetime.datetime.utcfromtimestamp(0)
                    if cloned_activity.timestamp:
                        reference = cloned_activity.timestamp
                    else:
                        reference = datetime.datetime.today()
                    delta = (reference - epoch).total_seconds() * 1000
                    cloned_activity.id = f"{prefix}{delta}"
                await self.log_activity(transcript, cloned_activity)
            return responses

        context.on_send_activities(send_activities_handler)

        # hook up update activity pipeline
        async def update_activity_handler(
            ctx: TurnContext, activity: Activity, next_update: Callable[[], Awaitable]
        ):
            # Run full pipeline
            response = await next_update()
            update_activity = copy.copy(activity)
            update_activity.type = ActivityTypes.message_update
            await self.log_activity(transcript, update_activity)
            return response

        context.on_update_activity(update_activity_handler)

        # hook up delete activity pipeline
        async def delete_activity_handler(
            ctx: TurnContext,
            reference: ConversationReference,
            next_delete: Callable[[], Awaitable],
        ):
            # Run full pipeline
            await next_delete()

            delete_msg = Activity(
                type=ActivityTypes.message_delete, id=reference.activity_id
            )
            deleted_activity: Activity = TurnContext.apply_conversation_reference(
                delete_msg, reference, False
            )
            await self.log_activity(transcript, deleted_activity)

        context.on_delete_activity(delete_activity_handler)

        if logic:
            await logic()

        # Flush transcript at end of turn
        while not transcript.empty():
            activity = transcript.get()
            if activity is None:
                break
            await self.logger.log_activity(activity)
            transcript.task_done()

    async def log_activity(self, transcript: Queue, activity: Activity) -> None:
        """Logs the activity.
        :param transcript: transcript.
        :param activity: Activity to log.
        """
        transcript.put(activity)


class TranscriptStore(TranscriptLogger):
    """Transcript storage for conversations."""

    @abstractmethod
    async def get_transcript_activities(
        self,
        channel_id: str,
        conversation_id: str,
        continuation_token: str,
        start_date: datetime,
    ) -> "PagedResult":
        """Get activities for a conversation (Aka the transcript).
        :param channel_id: Channel Id where conversation took place.
        :param conversation_id: Conversation ID
        :param continuation_token: Continuation token to page through results.
        :param start_date: Earliest time to include
        :result: Page of results of Activity objects
        """
        raise NotImplementedError

    @abstractmethod
    async def list_transcripts(
        self, channel_id: str, continuation_token: str
    ) -> "PagedResult":
        """List conversations in the channelId.
        :param channel_id: Channel Id where conversation took place.
        :param continuation_token : Continuation token to page through results.
        :result: Page of results of TranscriptInfo objects
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_transcript(self, channel_id: str, conversation_id: str) -> None:
        """Delete a specific conversation and all of it's activities.
        :param channel_id: Channel Id where conversation took place.
        :param conversation_id: Id of the conversation to delete.
        :result: None
        """
        raise NotImplementedError


class ConsoleTranscriptLogger(TranscriptLogger):
    """ConsoleTranscriptLogger writes activities to Console output."""

    async def log_activity(self, activity: Activity) -> None:
        """Log an activity to the transcript.
        :param activity:Activity being logged.
        """
        if activity:
            print(f"Activity Log: {activity}")
        else:
            raise TypeError("Activity is required")


class TranscriptInfo:
    """Metadata for a stored transcript."""

    # pylint: disable=invalid-name
    def __init__(
        self,
        channel_id: str = None,
        created: datetime = None,
        conversation_id: str = None,
    ):
        """
        :param channel_id: Channel ID the transcript was taken from
        :param created: Timestamp when event created
        :param id: Conversation ID
        """
        self.channel_id = channel_id
        self.created = created
        self.id = conversation_id


class PagedResult:
    """Paged results for transcript data."""

    # Page of Items
    items: List[object] = None
    # Token used to page through multiple pages.
    continuation_token: str = None
