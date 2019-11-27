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


class MessageActionsPayloadFrom(Model):
    """Represents a user, application, or conversation type that either sent or
    was referenced in a message.

    :param user: Represents details of the user.
    :type user: ~botframework.connector.teams.models.MessageActionsPayloadUser
    :param application: Represents details of the app.
    :type application:
     ~botframework.connector.teams.models.MessageActionsPayloadApp
    :param conversation: Represents details of the converesation.
    :type conversation:
     ~botframework.connector.teams.models.MessageActionsPayloadConversation
    """

    _attribute_map = {
        'user': {'key': 'user', 'type': 'MessageActionsPayloadUser'},
        'application': {'key': 'application', 'type': 'MessageActionsPayloadApp'},
        'conversation': {'key': 'conversation', 'type': 'MessageActionsPayloadConversation'},
    }

    def __init__(self, **kwargs):
        super(MessageActionsPayloadFrom, self).__init__(**kwargs)
        self.user = kwargs.get('user', None)
        self.application = kwargs.get('application', None)
        self.conversation = kwargs.get('conversation', None)
