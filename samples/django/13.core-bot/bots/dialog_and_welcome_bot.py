# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import os.path

from typing import List
from botbuilder.core import CardFactory
from botbuilder.core import ActivityHandler, ConversationState, UserState, TurnContext
from botbuilder.dialogs import Dialog
from botbuilder.schema import Activity, Attachment, ChannelAccount
from helpers.activity_helper import create_activity_reply

from .dialog_bot import DialogBot

class DialogAndWelcomeBot(DialogBot):

    def __init__(self, conversation_state: ConversationState, user_state: UserState, dialog: Dialog):
        super(DialogAndWelcomeBot, self).__init__(conversation_state, user_state, dialog)

    async def on_members_added_activity(self, members_added: List[ChannelAccount], turn_context: TurnContext):
        for member in members_added:
            # Greet anyone that was not the target (recipient) of this message.
            # To learn more about Adaptive Cards, see https://aka.ms/msbot-adaptivecards for more details.
            if member.id != turn_context.activity.recipient.id:
                welcome_card = self.create_adaptive_card_attachment()
                response = self.create_response(turn_context.activity, welcome_card)
                await turn_context.send_activity(response)
    
    # Create an attachment message response.
    def create_response(self, activity: Activity, attachment: Attachment):
        response = create_activity_reply(activity)
        response.attachments = [attachment]
        return response

    # Load attachment from file.
    def create_adaptive_card_attachment(self):
        relative_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(relative_path, "resources/welcomeCard.json")
        with open(path) as f:
            card = json.load(f)

        return Attachment(
            content_type= "application/vnd.microsoft.card.adaptive",
            content= card)