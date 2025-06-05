# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Union
from botbuilder.schema.sharepoint.card_view import (
    BaseCardComponent,
    CardComponentName,
    CardImage,
    CardButtonBase,
)


class CardTextInputIconButton(CardButtonBase):
    """
    Card Text Input Icon Button.

    :param icon: The icon to display on the button.
    :type icon: CardImage
    """

    _attribute_map = {
        "icon": {"key": "icon", "type": "CardImage"},
    }

    def __init__(self, *, icon: "CardImage" = None, **kwargs) -> None:
        super(CardTextInputIconButton, self).__init__(**kwargs)
        self.icon = icon


class CardTextInputTitleButton(CardButtonBase):
    """
    Card Text Input Title Button.

    :param title: The title to display on the button.
    :type title: str
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
    }

    def __init__(self, *, title: str = None, **kwargs) -> None:
        super(CardTextInputTitleButton, self).__init__(**kwargs)
        self.title = title


class CardTextInputComponent(BaseCardComponent):
    """
    Adaptive Card Extension Text input component. Represents a text input field rendered in the card view.

    :param component_name: The name of the component.
    :type component_name: CardComponentName
    :param placeholder: The placeholder text to display in the text input field.
    :type placeholder: str
    :param default_value: The default value to display in the text input field.
    :type default_value: str
    :param button: The button to display next to the text input field.
    :type button: CardTextInputIconButton or CardTextInputTitleButton
    :param icon_before: The icon to display before the text input field.
    :type icon_before: CardImage
    :param icon_after: The icon to display after the text input field.
    :type icon_after: CardImage
    """

    _attribute_map = {
        "placeholder": {"key": "placeholder", "type": "str"},
        "default_value": {"key": "defaultValue", "type": "str"},
        "button": {
            "key": "button",
            "type": "CardTextInputIconButton or CardTextInputTitleButton",
        },
        "icon_before": {"key": "iconBefore", "type": "CardImage"},
        "icon_after": {"key": "iconAfter", "type": "CardImage"},
    }

    def __init__(
        self,
        *,
        placeholder: str = None,
        default_value: str = None,
        button: Union["CardTextInputIconButton", "CardTextInputTitleButton"] = None,
        icon_before: "CardImage" = None,
        icon_after: "CardImage" = None,
        **kwargs
    ) -> None:
        super(CardTextInputComponent, self).__init__(
            component_name=CardComponentName.TextInput, **kwargs
        )
        self.placeholder = placeholder
        self.default_value = default_value
        self.button = button
        self.icon_before = icon_before
        self.icon_after = icon_after
