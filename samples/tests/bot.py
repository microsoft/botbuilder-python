"""
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""

from botbuilder.core import ActivityHandler, ConversationState, UserState, TurnContext, BotFrameworkAdapter, Storage, \
    BotFrameworkAdapterSettings
from botbuilder.dialogs import Dialog
from botbuilder.schema import Activity, Attachment
from flask import Response

from my_bot.api import MessagesHandler, NotifyHandler
from my_bot.dialogs import Dialog
from my_bot.helpers import create_activity_reply, run_dialog


def create_response(activity: Activity, attachment: Attachment = None) -> Activity:
    """
    Create an attachment message response.

    :param activity:
    :param attachment:
    :return:
    """
    response = create_activity_reply(activity)
    response.attachments = [attachment]
    return response

class ActivityHandler(LAFActivityHandler):
    """
    Activity Handler
    """

    def __init__(self, storage: Storage, settings: BotFrameworkAdapterSettings, loop):
        super(ActivityHandler, self).__init__(storage, settings, Dialog(), loop)

    async def on_turn(self, turn_context: TurnContext):
        """
        Echo User Input on Each turn

        :param turn_context:
        """
        # Check to see if this activity is an incoming message.
        # (It could theoretically be another type of activity.)
        if turn_context.activity.type == 'message' and turn_context.activity.text:
            # Check to see if the user sent a simple "quit" message.
            if turn_context.activity.text.lower() == 'quit':
                # Send a reply.
                await turn_context.send_activity('Bye!')
                exit(0)
            else:
                # Echo the message text back to the user.
                await turn_context.send_activity(f'I heard you say {turn_context.activity.text}')
