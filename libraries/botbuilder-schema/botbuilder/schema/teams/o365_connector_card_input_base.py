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


class O365ConnectorCardInputBase(Model):
    """O365 connector card input for ActionCard action.

    :param type: Input type name. Possible values include: 'textInput',
     'dateInput', 'multichoiceInput'
    :type type: str or ~botframework.connector.teams.models.enum
    :param id: Input Id. It must be unique per entire O365 connector card.
    :type id: str
    :param is_required: Define if this input is a required field. Default
     value is false.
    :type is_required: bool
    :param title: Input title that will be shown as the placeholder
    :type title: str
    :param value: Default value for this input field
    :type value: str
    """

    _attribute_map = {
        "type": {"key": "@type", "type": "str"},
        "id": {"key": "id", "type": "str"},
        "is_required": {"key": "isRequired", "type": "bool"},
        "title": {"key": "title", "type": "str"},
        "value": {"key": "value", "type": "str"},
    }

    def __init__(self, **kwargs):
        super(O365ConnectorCardInputBase, self).__init__(**kwargs)
        self.type = kwargs.get("type", None)
        self.id = kwargs.get("id", None)
        self.is_required = kwargs.get("is_required", None)
        self.title = kwargs.get("title", None)
        self.value = kwargs.get("value", None)
