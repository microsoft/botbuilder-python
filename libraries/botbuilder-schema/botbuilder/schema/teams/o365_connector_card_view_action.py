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

from .o365_connector_card_action_base import O365ConnectorCardActionBase


class O365ConnectorCardViewAction(O365ConnectorCardActionBase):
    """O365 connector card ViewAction action.

    :param type: Type of the action. Possible values include: 'ViewAction',
     'OpenUri', 'HttpPOST', 'ActionCard'
    :type type: str or ~botframework.connector.teams.models.enum
    :param name: Name of the action that will be used as button title
    :type name: str
    :param id: Action Id
    :type id: str
    :param target: Target urls, only the first url effective for card button
    :type target: list[str]
    """

    _attribute_map = {
        'type': {'key': '@type', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'id': {'key': '@id', 'type': 'str'},
        'target': {'key': 'target', 'type': '[str]'},
    }

    def __init__(self, **kwargs):
        super(O365ConnectorCardViewAction, self).__init__(**kwargs)
        self.target = kwargs.get('target', None)
