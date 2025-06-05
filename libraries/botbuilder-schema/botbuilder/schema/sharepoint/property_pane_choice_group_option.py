# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from msrest.serialization import Model

from botbuilder.schema.sharepoint.property_pane_field_properties import (
    PropertyPaneFieldProperties,
)


class PropertyPaneChoiceGroupIconProperties(Model):
    """
    SharePoint property pane choice group icon properties.

    :param office_fabric_icon_font_name: The Office Fabric icon font name.
    :type office_fabric_icon_font_name: str
    """

    _attribute_map = {
        "office_fabric_icon_font_name": {
            "key": "officeFabricIconFontName",
            "type": "str",
        },
    }

    def __init__(self, *, office_fabric_icon_font_name: str = None, **kwargs) -> None:
        super(PropertyPaneChoiceGroupIconProperties, self).__init__(**kwargs)
        self.office_fabric_icon_font_name = office_fabric_icon_font_name


class PropertyPaneChoiceGroupImageSize(Model):
    """
    SharePoint property pane choice group option.

    :param width: The width of the image.
    :type width: int
    :param height: The height of the image.
    :type height: int

    """

    _attribute_map = {
        "width": {"key": "width", "type": "int"},
        "height": {"key": "height", "type": "int"},
    }

    def __init__(self, *, width: int = None, height: int = None, **kwargs) -> None:
        super(PropertyPaneChoiceGroupImageSize, self).__init__(**kwargs)
        self.width = width
        self.height = height


class PropertyPaneChoiceGroupOption(Model):
    """
    SharePoint property pane choice group option.

    :param aria_label: The aria label of the choice group option.
    :type aria_label: str
    :param checked: The checked state of the choice group option.
    :type checked: bool
    :param disabled: The disabled state of the choice group option.
    :type disabled: bool
    :param icon_props: The icon properties of the choice group option.
    :type icon_props: PropertyPaneChoiceGroupIconProperties
    :param image_size: The image size of the choice group option.
    :type image_size: PropertyPaneChoiceGroupImageSize
    :param image_src: The image source of the choice group option.
    :type image_src: str
    :param key: The key of the choice group option.
    :type key: str
    :param text: The text of the choice group option.
    :type text: str
    """

    _attribute_map = {
        "aria_label": {"key": "ariaLabel", "type": "str"},
        "checked": {"key": "checked", "type": "bool"},
        "disabled": {"key": "disabled", "type": "bool"},
        "icon_props": {
            "key": "iconProps",
            "type": "PropertyPaneChoiceGroupIconProperties",
        },
        "image_size": {"key": "imageSize", "type": "PropertyPaneChoiceGroupImageSize"},
        "image_src": {"key": "imageSrc", "type": "str"},
        "key": {"key": "key", "type": "str"},
        "text": {"key": "text", "type": "str"},
    }

    def __init__(
        self,
        *,
        aria_label: str = None,
        checked: bool = False,
        disabled: bool = False,
        icon_props: PropertyPaneChoiceGroupIconProperties = None,
        image_size: PropertyPaneChoiceGroupImageSize = None,
        image_src: str = None,
        key: str = None,
        text: str = None,
        **kwargs
    ) -> None:
        super(PropertyPaneChoiceGroupOption, self).__init__(**kwargs)
        self.aria_label = aria_label
        self.checked = checked
        self.disabled = disabled
        self.icon_props = icon_props or PropertyPaneChoiceGroupIconProperties()
        self.image_size = image_size or PropertyPaneChoiceGroupImageSize()
        self.image_src = image_src
        self.key = key
        self.text = text


class PropertyPaneChoiceGroupProperties(PropertyPaneFieldProperties):
    """
    SharePoint property pane choice group field properties.

    :param aria_label: The aria label of the choice group.
    :type aria_label: str
    :param disabled: Indicates whether the choice group is disabled.
    :type disabled: bool
    :param options: The options of the choice group.
    :type options: list[PropertyPaneChoiceGroupOption]
    :param selected_key: The selected key of the choice group.
    :type selected_key: str
    """

    _attribute_map = {
        "label": {"key": "label", "type": "str"},
        "options": {"key": "options", "type": "[PropertyPaneChoiceGroupOption]"},
    }

    def __init__(
        self,
        *,
        label: str = None,
        options: List[PropertyPaneChoiceGroupOption] = None,
        **kwargs
    ) -> None:
        super(PropertyPaneChoiceGroupProperties, self).__init__(**kwargs)
        self.label = label
        self.options = options or []
