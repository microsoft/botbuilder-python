# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from botbuilder.core import MessageFactory, TurnContext, ActivityHandler
from botbuilder.schema import MessageReaction
from activity_log import ActivityLog


class MessageReactionBot(ActivityHandler):
    def __init__(self, activity_log: ActivityLog):
        self._log = activity_log

    async def on_reactions_added(
        self, message_reactions: List[MessageReaction], turn_context: TurnContext
    ):
        for reaction in message_reactions:
            activity = await self._log.find(turn_context.activity.reply_to_id)
            if not activity:
                await self._send_message_and_log_activity_id(
                    turn_context,
                    f"Activity {turn_context.activity.reply_to_id} not found in log",
                )
            else:
                await self._send_message_and_log_activity_id(
                    turn_context,
                    f"You added '{reaction.type}' regarding '{activity.text}'",
                )
        return

    async def on_reactions_removed(
        self, message_reactions: List[MessageReaction], turn_context: TurnContext
    ):
        for reaction in message_reactions:
            activity = await self._log.find(turn_context.activity.reply_to_id)
            if not activity:
                await self._send_message_and_log_activity_id(
                    turn_context,
                    f"Activity {turn_context.activity.reply_to_id} not found in log",
                )
            else:
                await self._send_message_and_log_activity_id(
                    turn_context,
                    f"You removed '{reaction.type}' regarding '{activity.text}'",
                )
        return

    async def on_message_activity(self, turn_context: TurnContext):
        await self._send_message_and_log_activity_id(
            turn_context, f"echo: {turn_context.activity.text}"
        )

    async def _send_message_and_log_activity_id(
        self, turn_context: TurnContext, text: str
    ):
        reply_activity = MessageFactory.text(text)
        resource_response = await turn_context.send_activity(reply_activity)

        await self._log.append(resource_response.id, reply_activity)
        return
