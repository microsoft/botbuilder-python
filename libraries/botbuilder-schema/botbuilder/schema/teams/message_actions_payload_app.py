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


class MessageActionsPayloadApp(Model):
    """Represents an application entity.

    :param application_identity_type: The type of application. Possible values
     include: 'aadApplication', 'bot', 'tenantBot', 'office365Connector',
     'webhook'
    :type application_identity_type: str or
     ~botframework.connector.teams.models.enum
    :param id: The id of the application.
    :type id: str
    :param display_name: The plaintext display name of the application.
    :type display_name: str
    """

    _attribute_map = {
        'application_identity_type': {'key': 'applicationIdentityType', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
        'display_name': {'key': 'displayName', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(MessageActionsPayloadApp, self).__init__(**kwargs)
        self.application_identity_type = kwargs.get('application_identity_type', None)
        self.id = kwargs.get('id', None)
        self.display_name = kwargs.get('display_name', None)
