# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import MessageFactory, TurnContext
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema import Mention


class MentionBot(TeamsActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        mention_data = {
            "mentioned": turn_context.activity.from_property,
            "text": f"<at>{turn_context.activity.from_property.name}</at>",
            "type": "mention",
        }

        mention_object = Mention(**mention_data)

        reply_activity = MessageFactory.text(f"Hello {mention_object.text}")
        reply_activity.entities = [mention_object]
        await turn_context.send_activity(reply_activity)
