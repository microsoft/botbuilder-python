# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MessageActionsPayloadConversation(Model):
    """Represents a team or channel entity.

    :param conversation_identity_type: The type of conversation, whether a
     team or channel. Possible values include: 'team', 'channel'
    :type conversation_identity_type: str or
     ~botframework.connector.teams.models.enum
    :param id: The id of the team or channel.
    :type id: str
    :param display_name: The plaintext display name of the team or channel
     entity.
    :type display_name: str
    """

    _attribute_map = {
        "conversation_identity_type": {
            "key": "conversationIdentityType",
            "type": "str",
        },
        "id": {"key": "id", "type": "str"},
        "display_name": {"key": "displayName", "type": "str"},
    }

    def __init__(self, **kwargs):
        super(MessageActionsPayloadConversation, self).__init__(**kwargs)
        self.conversation_identity_type = kwargs.get("conversation_identity_type", None)
        self.id = kwargs.get("id", None)
        self.display_name = kwargs.get("display_name", None)
