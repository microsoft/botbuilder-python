# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .turn_context import TurnContext
from .bot_state import BotState
from .storage import Storage


class ConversationState(BotState):
    """Conversation state
    Defines a state management object for conversation state.
    Extends `BootState` base class.

    .. remarks:: 
        Conversation state is available in any turn in a specific conversation, regardless of user, such as in a group conversation.
    """

    no_key_error_message = "ConversationState: channelId and/or conversation missing from context.activity."

    def __init__(self, storage: Storage):
        """ Creates a :class:ConversationState instance
        Creates a new instance of the :class:ConversationState class.
    
        :param storage: The storage containing the conversation state.
        :type storage: Storage 
        """
        super(ConversationState, self).__init__(storage, "ConversationState")

    def get_storage_key(self, turn_context: TurnContext) -> object:
        """ Get storage key
        Gets the key to use when reading and writing state to and from storage.

        :param turn_context: The context object for this turn.
        :type turn_context: TurnContext 

        :raise: TypeError if the `ITurnContext.Activity` for the current turn is missing 
        :any::Schema.Activity.ChannelId or :any::Schema.Activity.Conversation information, or 
        the conversation's :any::Schema.ConversationAccount.Id is missing.
        
        :return: The storage key.
        :rtype: str

        .. remarks:: 
            Conversation state includes the channel ID and conversation ID as part of its storage key.
        """
      
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
        """ Raise type error
        :raises: :class:TypeError This function raises exception.
        """
        raise TypeError(err)
