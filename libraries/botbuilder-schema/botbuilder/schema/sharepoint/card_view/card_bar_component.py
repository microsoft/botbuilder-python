# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema.sharepoint.card_view import (
    BaseCardComponent,
    CardComponentName,
    CardImage,
)


class CardBarComponent(BaseCardComponent):
    """
    Adaptive Card Extension Card view title area (card bar) component.

    :param component_name: The name of the component.
    :type component_name: CardComponentName
    :param title: The title to display.
    :type title: str
    :param icon: The icon to display.
    :type icon: CardImage
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "icon": {"key": "icon", "type": "CardImage"},
    }

    def __init__(
        self, *, title: str = None, icon: "CardImage" = None, **kwargs
    ) -> None:
        super(CardBarComponent, self).__init__(
            component_name=CardComponentName.CardBar, **kwargs
        )
        self.title = title
        self.icon = icon
