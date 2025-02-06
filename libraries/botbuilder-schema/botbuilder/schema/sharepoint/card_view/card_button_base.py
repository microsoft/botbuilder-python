# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model
from botbuilder.schema.sharepoint.actions.card_action import CardAction


class CardButtonBase(Model):
    """
    Base properties for the buttons used in different Adaptive Card Extension card view components,
    such as Text Input, Search Box and Card Button.

    :param action: The action to perform when the button is clicked.
    :type action: CardAction
    :param id: The Unique Id of the button.
    :type id: str
    """

    _attribute_map = {
        "action": {"key": "action", "type": "CardAction"},
        "id": {"key": "id", "type": "str"},
    }

    def __init__(self, *, action: CardAction = None, id: str = None, **kwargs) -> None:
        super(CardButtonBase, self).__init__(**kwargs)
        self.action = action
        self.id = id
