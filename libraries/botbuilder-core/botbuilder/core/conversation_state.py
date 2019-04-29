# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .turn_context import TurnContext
from .bot_state import BotState
from .storage import Storage


class ConversationState(BotState):
    """Conversation State
    Reads and writes conversation state for your bot to storage.
    """

    no_key_error_message = 'ConversationState: channelId and/or conversation missing from context.activity.'

    def __init__(self, storage: Storage):
        """Creates a new ConversationState instance.
        Parameters
        ----------
        storage : Storage
            Where to store 
        namespace: str
        """
        def call_get_storage_key(context):
            key = self.get_storage_key(context)
            if key is None:
                raise AttributeError(self.no_key_error_message)
            else:
                return key

        super(ConversationState, self).__init__(storage, 'ConversationState')


    def get_storage_key(self, context: TurnContext):
        activity = context.activity
        channel_id = getattr(activity, 'channel_id', None)
        conversation_id = getattr(activity.conversation, 'id', None) if hasattr(activity, 'conversation') else None

        storage_key = None
        if channel_id and conversation_id:
            storage_key = "%s/conversations/%s" % (channel_id,conversation_id)
        return storage_key
