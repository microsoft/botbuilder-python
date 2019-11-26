# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC


class ChannelApiMethods(ABC):
    REPLY_TO_ACTIVITY = "ReplyToActivity"
    SEND_TO_CONVERSATION = "SendtoConversation"
    UPDATE_ACTIVITY = "UpdateActivity"
    DELETE_ACTIVITY = "DeleteActivity"
    SEND_CONVERSATION_HISTORY = "SendConversationHistory"
    GET_CONVERSATION_MEMBERS = "GetConversationMembers"
    GET_CONVERSATION_PAGED_MEMBERS = "GetConversationPagedMembers"
    DELETE_CONVERSATION_MEMBER = "DeleteConversationMember"
    GET_ACTIVITY_MEMBERS = "GetActivityMembers"
    UPLOAD_ATTACHMENT = "UploadAttachment"
    CREATE_CONVERSATION = "CreateConversation"
    GET_CONVERSATIONS = "GetConversations"
