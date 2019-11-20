# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import MessageFactory, TurnContext, ChannelAccount
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema import Mention


class MentionBot(TeamsActivityHandler):
   async def on_message_activity(turn_context: TurnContext):
        m = {
            "mentioned": turn_context.activity.from, 
            "text": f"<at>{turn_context.activity.from.name}</at>",
            "type": "mention"
           }
        
        reply_activity = MessageFactory.text(f"Hello {m.text}")
        reply_activity.entities = [Mention(**m)]
        await turn_context.send_activity(reply_activity)
