# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model
from enum import IntEnum


class PopupWindowPosition(IntEnum):
    """
    SharePoint property pane link popup window position
    """

    Center = 0
    """ The popup window is displayed at the top. """
    RightTop = 1
    """ The popup window is displayed at the right. """
    LeftTop = 2
    """ The popup window is displayed at the left. """
    RightBottom = 3
    """ The popup window is displayed at the right. """
    LeftBottom = 4
    """ The popup window is displayed at the center. """


class PropertyPaneLinkPopupWindowProperties(Model):
    """
    SharePoint property pane link popup window properties.

    :param height: The height of the popup window.
    :type height: int
    :param position_window_position: The position of the popup window.
    :type position_window_position: PopupWindowPosition
    :param title: The title of the popup window.
    :type title: str
    :param width: The width of the popup window.
    :type width: int
    """

    _attribute_map = {
        "height": {"key": "height", "type": "int"},
        "position_window_position": {
            "key": "positionWindowPosition",
            "type": "PopupWindowPosition",
        },
        "title": {"key": "title", "type": "str"},
        "width": {"key": "width", "type": "int"},
    }

    def __init__(
        self,
        *,
        height: int = None,
        position_window_position: PopupWindowPosition = None,
        title: str = "",
        width: int = None,
        **kwargs
    ) -> None:
        super(PropertyPaneLinkPopupWindowProperties, self).__init__(**kwargs)
        self.height = height
        self.position_window_position = position_window_position
        self.title = title
        self.width = width
