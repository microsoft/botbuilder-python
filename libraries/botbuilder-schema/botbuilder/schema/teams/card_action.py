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


class CardAction(Model):
    """An action on a card.

    :param type: Defines the type of action implemented by this button.
    :type type: str
    :param title: Text description which appear on the button.
    :type title: str
    :param image: URL Picture which will appear on the button, next to text
     label.
    :type image: str
    :param value: Supplementary parameter for action. Content of this property
     depends on the ActionType
    :type value: object
    """

    _attribute_map = {
        "type": {"key": "type", "type": "str"},
        "title": {"key": "title", "type": "str"},
        "image": {"key": "image", "type": "str"},
        "value": {"key": "value", "type": "object"},
    }

    def __init__(self, **kwargs):
        super(CardAction, self).__init__(**kwargs)
        self.type = kwargs.get("type", None)
        self.title = kwargs.get("title", None)
        self.image = kwargs.get("image", None)
        self.value = kwargs.get("value", None)
