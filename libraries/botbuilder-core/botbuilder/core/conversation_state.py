# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .turn_context import TurnContext
from .bot_state import BotState
from .storage import Storage


class ConversationState(BotState):
    """Conversation State
    Reads and writes conversation state for your bot to storage.
    """

    no_key_error_message = "ConversationState: channelId and/or conversation missing from context.activity."

    def __init__(self, storage: Storage):
        super(ConversationState, self).__init__(storage, "ConversationState")

    def get_storage_key(self, turn_context: TurnContext) -> object:
        channel_id = turn_context.activity.channel_id or self.__raise_type_error(
            "invalid activity-missing channel_id"
        )
        conversation_id = (
            turn_context.activity.conversation.id
            or self.__raise_type_error("invalid activity-missing conversation.id")
        )

        storage_key = None
        if channel_id and conversation_id:
            storage_key = "%s/conversations/%s" % (channel_id, conversation_id)
        return storage_key

    def __raise_type_error(self, err: str = "NoneType found while expecting value"):
        raise TypeError(err)
