# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum
from botbuilder.schema.sharepoint.actions.card_action import CardAction
from botbuilder.schema.sharepoint.card_view import (
    BaseCardComponent,
    CardComponentName,
    CardButtonBase,
)


class CardButtonStyle(str, Enum):
    """
    The style of the button.
    """

    Default = "Default"
    """ Default style """
    Positive = "Positive"
    """ Positive (primary) style. """


class CardButtonComponent(BaseCardComponent, CardButtonBase):
    """
    Adaptive Card Extension Card view button component.

    :param component_name: The name of the component.
    :type component_name: CardComponentName
    :param action: The action to perform when the button is clicked.
    :type action: CardAction
    :param title: Text displayed on the button.
    :type title: str
    :param style: The style of the button.
    :type style: CardButtonStyle
    """

    _attribute_map = {
        "action": {"key": "action", "type": "CardAction"},
        "title": {"key": "title", "type": "str"},
        "style": {"key": "style", "type": "CardButtonStyle"},
    }

    def __init__(
        self,
        *,
        action: CardAction = None,
        title: str = None,
        style: CardButtonStyle = None,
        **kwargs
    ) -> None:
        super(CardButtonComponent, self).__init__(
            component_name=CardComponentName.CardButton, **kwargs
        )
        self.action = action
        self.title = title
        self.style = style
