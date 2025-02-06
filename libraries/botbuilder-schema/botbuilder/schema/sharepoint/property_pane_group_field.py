# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import IntEnum
from msrest.serialization import Model

from botbuilder.schema.sharepoint.property_pane_field_properties import (
    PropertyPaneFieldProperties,
)


class FieldType(IntEnum):
    """
    SharePoint property pane group field type.
    """

    CheckBox = 2
    TextField = 3
    Toggle = 5
    Dropdown = 6
    Label = 7
    Slider = 8
    ChoiceGroup = 10
    HorizontalRule = 12
    Link = 13


class PropertyPaneGroupField(Model):
    """
    SharePoint property pane group field.

    :param type: The type of the field.
    :type type: FieldType
    :param properties: The properties of the field.
    :type properties: PropertyPaneFieldProperties
    :param should_focus: Indicates whether the field should be focused.
    :type should_focus: bool
    :param target_property: The target property of the field.
    :type target_property: str
    """

    _attribute_map = {
        "type": {"key": "type", "type": "FieldType"},
        "properties": {"key": "properties", "type": "PropertyPaneFieldProperties"},
        "should_focus": {"key": "shouldFocus", "type": "bool"},
        "target_property": {"key": "targetProperty", "type": "str"},
    }

    def __init__(
        self,
        *,
        type: FieldType = None,
        properties: PropertyPaneFieldProperties = None,
        should_focus: bool = False,
        target_property: str = None,
        **kwargs
    ) -> None:
        super(PropertyPaneGroupField, self).__init__(**kwargs)
        self.type = type
        self.properties = properties
        self.should_focus = should_focus
        self.target_property = target_property
