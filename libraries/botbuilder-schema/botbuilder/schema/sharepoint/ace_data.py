# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum
from typing import Optional
from msrest.serialization import Model


class AceCardSize(str, Enum):
    """
    This enum contains the different types of card templates available in the SPFx framework.
    """

    MEDIUM = "Medium"
    LARGE = "Large"


class AceData(Model):
    """
    SharePoint Ace Data object.

    :param card_size: The size of the card.
    :type card_size: AceCardSize
    :param data_version: The version of the data.
    :type data_version: str
    :param id: The ID of the card.
    :type id: str
    :param title: The title of the card.
    :type title: str
    :param description: The description of the card.
    :type description: str
    :param icon_property: The icon property of the card.
    :type icon_property: str
    :param is_visible: A flag indicating whether the card is visible.
    :type is_visible: bool
    :param properties: The properties of the card.
    :type properties: object


    """

    _attribute_map = {
        "card_size": {"key": "cardSize", "type": "AceCardSize"},
        "data_version": {"key": "dataVersion", "type": "str"},
        "id": {"key": "id", "type": "str"},
        "title": {"key": "title", "type": "str"},
        "description": {"key": "description", "type": "str"},
        "icon_property": {"key": "iconProperty", "type": "str"},
        "is_visible": {"key": "isVisible", "type": "bool"},
        "properties": {"key": "properties", "type": "object"},
    }

    def __init__(
        self,
        *,
        card_size: AceCardSize = None,
        data_version: str = None,
        id: str = None,
        title: str = None,
        description: str = None,
        icon_property: str = None,
        is_visible: Optional[bool] = None,
        properties: object = None,
        **kwargs
    ) -> None:
        super(AceData, self).__init__(**kwargs)
        self.card_size = card_size
        self.data_version = data_version
        self.id = id
        self.title = title
        self.description = description
        self.icon_property = icon_property
        self.is_visible = is_visible
        self.properties = properties
