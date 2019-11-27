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

from .o365_connector_card_input_base_py3 import O365ConnectorCardInputBase


class O365ConnectorCardMultichoiceInput(O365ConnectorCardInputBase):
    """O365 connector card multiple choice input.

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
    :param choices: Set of choices whose each item can be in any subtype of
     O365ConnectorCardMultichoiceInputChoice.
    :type choices:
     list[~botframework.connector.teams.models.O365ConnectorCardMultichoiceInputChoice]
    :param style: Choice item rendering style. Default value is 'compact'.
     Possible values include: 'compact', 'expanded'
    :type style: str or ~botframework.connector.teams.models.enum
    :param is_multi_select: Define if this input field allows multiple
     selections. Default value is false.
    :type is_multi_select: bool
    """

    _attribute_map = {
        "type": {"key": "@type", "type": "str"},
        "id": {"key": "id", "type": "str"},
        "is_required": {"key": "isRequired", "type": "bool"},
        "title": {"key": "title", "type": "str"},
        "value": {"key": "value", "type": "str"},
        "choices": {
            "key": "choices",
            "type": "[O365ConnectorCardMultichoiceInputChoice]",
        },
        "style": {"key": "style", "type": "str"},
        "is_multi_select": {"key": "isMultiSelect", "type": "bool"},
    }

    def __init__(
        self,
        *,
        type=None,
        id: str = None,
        is_required: bool = None,
        title: str = None,
        value: str = None,
        choices=None,
        style=None,
        is_multi_select: bool = None,
        **kwargs
    ) -> None:
        super(O365ConnectorCardMultichoiceInput, self).__init__(
            type=type,
            id=id,
            is_required=is_required,
            title=title,
            value=value,
            **kwargs
        )
        self.choices = choices
        self.style = style
        self.is_multi_select = is_multi_select
