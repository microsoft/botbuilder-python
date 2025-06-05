# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema.sharepoint.property_pane_field_properties import (
    PropertyPaneFieldProperties,
)


class PropertyPaneCheckboxProperties(PropertyPaneFieldProperties):
    """
    SharePoint property pane checkbox field properties.

    :param text: The text to display next to the checkbox.
    :type text: str
    :param disabled: Whether or not the checkbox is disabled.
    :type disabled: bool
    :param checked: Whether or not the checkbox is checked.
    :type checked: bool
    """

    _attribute_map = {
        "text": {"key": "text", "type": "str"},
        "disabled": {"key": "disabled", "type": "bool"},
        "checked": {"key": "checked", "type": "bool"},
    }

    def __init__(
        self,
        *,
        text: str = None,
        disabled: bool = False,
        checked: bool = None,
        **kwargs
    ) -> None:
        super(PropertyPaneCheckboxProperties, self).__init__(**kwargs)
        self.text = text
        self.disabled = disabled
        self.checked = checked
