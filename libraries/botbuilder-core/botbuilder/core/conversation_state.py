# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .bot_context import BotContext
from .bot_state import BotState
from .storage import Storage


class ConversationState(BotState):
    """
    Reads and writes conversation state for your bot to storage.
    """

    no_key_error_message = 'ConversationState: channelId and/or conversation missing from context.activity.'

    def __init__(self, storage: Storage, namespace: str=''):
        """
        Creates a new ConversationState instance.
        :param storage:
        :param namespace:
        """

        def call_get_storage_key(context):
            key = self.get_storage_key(context)
            if key is None:
                raise AttributeError(self.no_key_error_message)
            else:
                return key

        super(ConversationState, self).__init__(storage, call_get_storage_key)
        self.namespace = namespace

    def get_storage_key(self, context: BotContext):
        activity = context.activity
        channel_id = activity.channel_id
        conversation_id = (activity.conversation.id if
                           (activity and hasattr(activity, 'conversation') and hasattr(activity.conversation, 'id')) else
                           None)
        return f"conversation/{channel_id}/{conversation_id}" if channel_id and conversation_id else None
