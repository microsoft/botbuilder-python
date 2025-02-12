# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema.sharepoint.property_pane_field_properties import (
    PropertyPaneFieldProperties,
)


class PropertyPaneToggleProperties(PropertyPaneFieldProperties):
    """
    SharePoint property pane toggle properties.

    :param aria_label: The aria label of the toggle.
    :type aria_label: str
    :param label: The label of the toggle.
    :type label: str
    :param disabled: Indicates whether the toggle is disabled.
    :type disabled: bool
    :param checked: Indicates whether the toggle is checked.
    :type checked: bool
    :param key: The key of the toggle.
    :type key: str
    :param off_text: The text to display when the toggle is off.
    :type off_text: str
    :param on_text: The text to display when the toggle is on.
    :type on_text: str
    :param off_aria_label: The aria label of the toggle when it is off.
    :type off_aria_label: str
    :param on_aria_label: The aria label of the toggle when it is on.
    :type on_aria_label: str
    """

    _attribute_map = {
        "area_label": {"key": "areaLabel", "type": "str"},
        "label": {"key": "label", "type": "str"},
        "disabled": {"key": "disabled", "type": "bool"},
        "checked": {"key": "checked", "type": "bool"},
        "key": {"key": "key", "type": "str"},
        "off_text": {"key": "offText", "type": "str"},
        "on_text": {"key": "onText", "type": "str"},
        "off_aria_label": {"key": "offAriaLabel", "type": "str"},
        "on_aria_label": {"key": "onAriaLabel", "type": "str"},
    }

    def __init__(
        self,
        *,
        aria_label: str = None,
        label: str = None,
        disabled: bool = False,
        checked: bool = False,
        key: str = None,
        off_text: str = None,
        on_text: str = None,
        off_aria_label: str = None,
        on_aria_label: str = None,
        **kwargs
    ) -> None:
        super(PropertyPaneToggleProperties, self).__init__(**kwargs)
        self.aria_label = aria_label
        self.label = label
        self.disabled = disabled
        self.checked = checked
        self.key = key
        self.off_text = off_text
        self.on_text = on_text
        self.off_aria_label = off_aria_label
        self.on_aria_label = on_aria_label
