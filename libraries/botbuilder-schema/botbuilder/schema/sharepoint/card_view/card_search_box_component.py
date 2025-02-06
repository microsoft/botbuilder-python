# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema.sharepoint.card_view import (
    BaseCardComponent,
    CardComponentName,
    CardButtonBase,
)
from botbuilder.schema.sharepoint.actions.card_action import CardAction


class CardSearchBoxButton(CardButtonBase):
    """
    Card Search box button.

    :param action: The action to perform when the button is clicked.
    :type action: CardAction
    :param id: The Unique Id of the button.
    :type id: str
    """

    _attribute_map = {}

    def __init__(self, *, action: CardAction = None, id: str = None, **kwargs) -> None:
        super(CardSearchBoxButton, self).__init__(action=action, id=id, **kwargs)


class CardSearchBoxComponent(BaseCardComponent):
    """
    Adaptive Card Extension Search box component. Represents a search box rendered in the card view.

    :param component_name: The name of the component.
    :type component_name: CardComponentName
    :param placeholder: The placeholder text to display in the search box.
    :type placeholder: str
    :param default_value: The default value to display in the search box.
    :type default_value: str
    :param button: The button to display next to the search box.
    :type button: CardSearchBoxButton
    """

    _attribute_map = {
        "placeholder": {"key": "placeholder", "type": "str"},
        "default_value": {"key": "defaultValue", "type": "str"},
        "button": {"key": "button", "type": "CardSearchBoxButton"},
    }

    def __init__(
        self,
        *,
        placeholder: str = None,
        default_value: str = None,
        button: "CardSearchBoxButton" = None,
        **kwargs
    ) -> None:
        super(CardSearchBoxComponent, self).__init__(
            component_name=CardComponentName.SearchBox, **kwargs
        )
        self.placeholder = placeholder
        self.default_value = default_value
        self.button = button
