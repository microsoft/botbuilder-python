# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema.sharepoint.property_pane_field_properties import (
    PropertyPaneFieldProperties,
)


class PropertyPaneLinkProperties(PropertyPaneFieldProperties):
    """
    SharePoint property pane label properties.

    :param text: The text of the link.
    :type text: str
    :param required: Indicates whether the link is required.
    :type required: bool
    """

    # Mapping of class attributes to their serialized keys
    _attribute_map = {
        "text": {"key": "text", "type": "str"},
        "required": {"key": "required", "type": "bool"},
    }

    def __init__(self, text: str = None, required: bool = False, **kwargs) -> None:
        super(PropertyPaneLinkProperties, self).__init__(**kwargs)
        self.text = text
        self.required = required
