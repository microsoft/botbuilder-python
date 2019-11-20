# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import MessageFactory, TurnContext, ActivityHandler
from botbuilder.schema import ActivityTypes

class ActivitiyUpdateAndDeleteBot(ActivityHandler):
    def __init__(self):
        self.activity_ids = []

    async def on_message_activity(self, turn_context: TurnContext):
        TurnContext.remove_recipient_mention(turn_context.activity)
        if turn_context.activity.text == "delete":
            for activity in self.activity_ids:
                await turn_context.delete_activity(activity)
            
            self.activity_ids = []
        else:
            await self._send_message_and_log_activity_id(turn_context, turn_context.activity.text)

            for activity_id in self.activity_ids:
                new_activity = MessageFactory.text(turn_context.activity.text)
                new_activity.id = activity_id
                await turn_context.update_activity(new_activity)
    
    async def _send_message_and_log_activity_id(self, turn_context: TurnContext, text: str):
        reply_activity = MessageFactory.text(text)
        resource_response = await turn_context.send_activity(reply_activity)
        self.activity_ids.append(resource_response.id)
