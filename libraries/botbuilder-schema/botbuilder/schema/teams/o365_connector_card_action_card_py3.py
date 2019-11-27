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


class O365ConnectorCardActionCard(O365ConnectorCardActionBase):
    """O365 connector card ActionCard action.

    :param type: Type of the action. Possible values include: 'ViewAction',
     'OpenUri', 'HttpPOST', 'ActionCard'
    :type type: str or ~botframework.connector.teams.models.enum
    :param name: Name of the action that will be used as button title
    :type name: str
    :param id: Action Id
    :type id: str
    :param inputs: Set of inputs contained in this ActionCard whose each item
     can be in any subtype of O365ConnectorCardInputBase
    :type inputs:
     list[~botframework.connector.teams.models.O365ConnectorCardInputBase]
    :param actions: Set of actions contained in this ActionCard whose each
     item can be in any subtype of O365ConnectorCardActionBase except
     O365ConnectorCardActionCard, as nested ActionCard is forbidden.
    :type actions:
     list[~botframework.connector.teams.models.O365ConnectorCardActionBase]
    """

    _attribute_map = {
        "type": {"key": "@type", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "id": {"key": "@id", "type": "str"},
        "inputs": {"key": "inputs", "type": "[O365ConnectorCardInputBase]"},
        "actions": {"key": "actions", "type": "[O365ConnectorCardActionBase]"},
    }

    def __init__(
        self,
        *,
        type=None,
        name: str = None,
        id: str = None,
        inputs=None,
        actions=None,
        **kwargs
    ) -> None:
        super(O365ConnectorCardActionCard, self).__init__(
            type=type, name=name, id=id, **kwargs
        )
        self.inputs = inputs
        self.actions = actions
