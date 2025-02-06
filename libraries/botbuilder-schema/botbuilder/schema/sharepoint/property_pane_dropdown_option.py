# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import IntEnum
from msrest.serialization import Model


class DropDownOptionType(IntEnum):
    """
    SharePoint property pane dropdown option type
    """

    Normal = 0
    """ The dropdown option is normal. """
    Divider = 1
    """ The dropdown option is a divider. """
    Header = 2
    """ The dropdown option is a header. """


class PropertyPaneDropDownOption(Model):
    """
    harePoint property pane drop down option.

    :param index: The index of the drop down option.
    :type index: int
    :param key: The key of the drop down option.
    :type key: str
    :param text: The text of the drop down option.
    :type text: str
    :param type: The type of the drop down option.
    :type type: DropDownOptionType
    """

    _attribute_map = {
        "index": {"key": "index", "type": "int"},
        "key": {"key": "key", "type": "str"},
        "text": {"key": "text", "type": "str"},
        "type": {"key": "type", "type": "DropDownOptionType"},
    }

    def __init__(
        self,
        *,
        index: int = 0,
        key: str = "",
        text: str = "",
        type: DropDownOptionType = None,
        **kwargs
    ) -> None:
        super(PropertyPaneDropDownOption, self).__init__(**kwargs)
        self.index = index
        self.key = key
        self.text = text
        self.type = type
