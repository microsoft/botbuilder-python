# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import (
    ChannelAccount,
    Activity,
    ActivityTypes,
    EndOfConversationCodes,
)


class EchoBot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):
        if "end" in turn_context.activity.text or "stop" in turn_context.activity.text:
            await turn_context.send_activity("ending conversation from the skill...")
            end_of_conversation = Activity(
                type=ActivityTypes.end_of_conversation,
                code=EndOfConversationCodes.completed_successfully,
            )
            await turn_context.send_activity(end_of_conversation)
        else:
            await turn_context.send_activity(
                f"Echo: (Python) : {turn_context.activity.text}"
            )
            await turn_context.send_activity(
                'Say "end" or "stop" and I\'ll end the conversation and back to the parent.'
            )
