# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema.sharepoint.card_view import BaseCardComponent, CardComponentName


class CardTextComponent(BaseCardComponent):
    """
    Adaptive Card Extension Text component. Represents a text block rendered in the card view.

    :param component_name: The name of the component.
    :type component_name: CardComponentName
    :param text: The text to display.
    :type text: str
    """

    _attribute_map = {
        "text": {"key": "text", "type": "str"},
    }

    def __init__(self, *, text: str = None, **kwargs) -> None:
        super(CardTextComponent, self).__init__(
            component_name=CardComponentName.Text, **kwargs
        )
        self.text = text
