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

from .o365_connector_card_action_base_py3 import O365ConnectorCardActionBase


class O365ConnectorCardHttpPOST(O365ConnectorCardActionBase):
    """O365 connector card HttpPOST action.

    :param type: Type of the action. Possible values include: 'ViewAction',
     'OpenUri', 'HttpPOST', 'ActionCard'
    :type type: str or ~botframework.connector.teams.models.enum
    :param name: Name of the action that will be used as button title
    :type name: str
    :param id: Action Id
    :type id: str
    :param body: Content to be posted back to bots via invoke
    :type body: str
    """

    _attribute_map = {
        "type": {"key": "@type", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "id": {"key": "@id", "type": "str"},
        "body": {"key": "body", "type": "str"},
    }

    def __init__(
        self, *, type=None, name: str = None, id: str = None, body: str = None, **kwargs
    ) -> None:
        super(O365ConnectorCardHttpPOST, self).__init__(
            type=type, name=name, id=id, **kwargs
        )
        self.body = body
