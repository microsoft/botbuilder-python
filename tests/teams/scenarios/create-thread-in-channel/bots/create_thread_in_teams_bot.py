# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import MessageFactory, TurnContext
from botbuilder.core.teams import (
    teams_get_channel_id,
    TeamsActivityHandler, 
    TeamsInfo
)


class CreateThreadInTeamsBot(TeamsActivityHandler):
    def __init__(self, id):
        self.id = id

    async def on_message_activity(self, turn_context: TurnContext):
        message = MessageFactory.text("first message")
        channel_id = teams_get_channel_id(turn_context.activity)
        result = await TeamsInfo.send_message_to_teams_channel(turn_context, message, channel_id)

        await turn_context.adapter.continue_conversation(result[0], self._continue_conversation_callback, self.id)
    
    async def _continue_conversation_callback(self, turn_context):
        await turn_context.send_activity(MessageFactory.text("second message"))
