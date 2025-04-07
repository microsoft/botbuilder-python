# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema.sharepoint.card_view import BaseCardComponent, CardComponentName
from botbuilder.schema.sharepoint.actions import CardAction


class CardSearchFooterComponent(BaseCardComponent):
    """
    Adaptive Card Extension Search footer component. Represents a footer rendered in the card view.

    :param component_name: The name of the component.
    :type component_name: CardComponentName
    :param title: The title to display.
    :type title: str
    :param image_url: The URL of the image to display.
    :type image_url: str
    :param image_initials: The initials to display on the image.
    :type image_initials: str
    :param text: The text to display.
    :type text: str
    :param on_selection: The action to perform when the footer is selected.
    :type on_selection: CardAction
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "image_url": {"key": "imageUrl", "type": "str"},
        "image_initials": {"key": "imageInitials", "type": "str"},
        "text": {"key": "text", "type": "str"},
        "on_selection": {"key": "onSelection", "type": "CardAction"},
    }

    def __init__(
        self,
        *,
        title: str = None,
        image_url: str = None,
        image_initials: str = None,
        text: str = None,
        on_selection: CardAction = None,
        **kwargs
    ) -> None:
        super(CardSearchFooterComponent, self).__init__(
            component_name=CardComponentName.SearchFooter, **kwargs
        )
        self.title = title
        self.image_url = image_url
        self.image_initials = image_initials
        self.text = text
        self.on_selection = on_selection
