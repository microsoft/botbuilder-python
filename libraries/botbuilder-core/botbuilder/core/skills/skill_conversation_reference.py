# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from botbuilder.schema import ConversationReference


class SkillConversationReference:
    """
    ConversationReference implementation for Skills ConversationIdFactory.
    """

    def __init__(self, conversation_reference: ConversationReference, oauth_scope: str):
        self.conversation_reference = conversation_reference
        self.oauth_scope = oauth_scope
