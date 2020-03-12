# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import uuid

from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    MessageFactory,
)
from botbuilder.integration import BotFrameworkHttpClient

from botbuilder.schema import DeliveryModes


class ParentBot(ActivityHandler):
    def __init__(
        self, skill_client: BotFrameworkHttpClient,
    ):
        self.client = skill_client

    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity("parent: before child")

        activity = MessageFactory.text("parent to child")
        TurnContext.apply_conversation_reference(
            activity, TurnContext.get_conversation_reference(turn_context.activity)
        )
        activity.delivery_mode = DeliveryModes.expect_replies

        activities = await self.client.post_buffered_activity(
            None,
            "toBotId",
            "http://localhost:3979/api/messages",
            "http://tempuri.org/whatever",
            str(uuid.uuid4()),
            activity,
        )

        if activities:
            await turn_context.send_activities(activities)

        await turn_context.send_activity("parent: after child")
