# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


def get_conversation_reference(activity):
    return {
        'activityId': activity['id'],
        'user': activity['from'],
        'bot': activity['recipient'],
        'conversation': activity['conversation'],
        'channelId': activity['channelId'],
        'serviceUrl': activity['serviceUrl']
    }


def apply_conversation_reference(activity, reference):
    activity['channelId'] = reference['channelId']
    activity['serviceUrl'] = reference['serviceUrl']
    activity['conversation'] = reference['conversation']
    activity['from'] = reference['bot']
    activity['recipient'] = reference['user']
    activity['replyToId'] = reference['activityId']


END_OF_CONVERSATION_CODES = {
    """Codes indicating why a conversation has ended."""

    'unknown': 'unknown',
    """The conversation was ended for unknown reasons."""
    
    'completedSuccessfully': 'completedSuccessfully',
    """The conversation completed successfully."""

    'userCancelled': 'userCancelled',
    """The user cancelled the conversation."""

    'botTimedOut': 'botTimedOut',
    """The conversation was ended because requests sent to the bot timed out."""
    
    'botIssuedInvalidMessage': 'botIssuedInvalidMessage',
    """The conversation was ended because the bot sent an invalid message."""
    
    'channelFailed': 'channelFailed',
    """The conversation ended because the channel experienced an internal failure."""

    'unrecognized': 'unrecognized'
    """The conversation ended because the bot didn't recognize the users utterance."""
}

ATTACHMENT_LAYOUTS = {
    """Desired layout style for a list of attachments sent to a user."""
    
    'list': 'list',
    """Attachments should be rendered as a list."""
    
    'carousel': 'carousel'
    """Attachments should be rendered using a carousel layout."""
}

TEXT_FORMATS = {
    """Desired text format for a message being sent to a user."""
    
    'plain': 'plain',
    """Message text should be rendered as plain text."""
    
    'markdown': 'markdown'
    """Message text should be rendered using markdown."""
}


ACTIVITY_TYPES = {
    """List of activity types supported by the Bot Framework."""
    
    'contactRelationUpdate': 'contactRelationUpdate',
    """A user has added/removed the bot as a contact."""

    'conversationUpdate': 'conversationUpdate',
    """User(s) have either joined or left the conversation."""

    'endOfConversation': 'endOfConversation',
    """The conversation is being ended by either the bot or user."""

    'event': 'event',
    """A named event sent from or to a client."""

    'invoke': 'invoke',
    """An operation is being invoked."""

    'message': 'message',
    """A message sent from or to a user/group."""
    
    'messageReaction': 'messageReaction',
    """A message activity within a conversation has had a message reaction added or removed."""
    
    'typing': 'typing'
    """An indicator that the bot is typing. Should be periodically resent every few seconds."""
}
