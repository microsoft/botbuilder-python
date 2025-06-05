# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.schema.sharepoint.property_pane_dropdown_option import (
    PropertyPaneDropDownOption,
)
from botbuilder.schema.sharepoint.property_pane_field_properties import (
    PropertyPaneFieldProperties,
)


class PropertyPaneDropDownProperties(PropertyPaneFieldProperties):
    """
    SharePoint property pane dropdown field properties.

    :param aria_label: The aria label of the dropdown.
    :type aria_label: str
    :param aria_position_in_set: The position in the set of the dropdown.
    :type aria_position_in_set: int
    :param aria_set_size: The size of the set of the dropdown.
    :type aria_set_size: int
    :param label: The label of the dropdown.
    :type label: str
    :param disabled: Indicates whether the dropdown is disabled.
    :type disabled: bool
    :param error_message: The error message of the dropdown.
    :type error_message: str
    :param selected_key: The selected key of the dropdown.
    :type selected_key: str
    :param options: The options of the dropdown.
    :type options: list[PropertyPaneDropDownOption]
    """

    # Mapping of class attributes to their serialized keys
    _attribute_map = {
        "aria_label": {"key": "ariaLabel", "type": "str"},
        "aria_position_in_set": {"key": "ariaPositionInSet", "type": "int"},
        "aria_set_size": {"key": "ariaSetSize", "type": "int"},
        "label": {"key": "label", "type": "str"},
        "disabled": {"key": "disabled", "type": "bool"},
        "error_message": {"key": "errorMessage", "type": "str"},
        "selected_key": {"key": "selectedKey", "type": "str"},
        "options": {"key": "options", "type": "[PropertyPaneDropDownOption]"},
    }

    def __init__(
        self,
        aria_label: str = "",
        aria_position_in_set: int = 1,
        aria_set_size: int = 0,
        label: str = "",
        disabled: bool = False,
        error_message: str = "",
        selected_key: str = "",
        options: List[PropertyPaneDropDownOption] = None,
        **kwargs
    ) -> None:
        super(PropertyPaneDropDownProperties, self).__init__(**kwargs)
        self.aria_label = aria_label
        self.aria_position_in_set = aria_position_in_set
        self.aria_set_size = aria_set_size
        self.label = label
        self.disabled = disabled
        self.error_message = error_message
        self.selected_key = selected_key
        self.options = options or []
