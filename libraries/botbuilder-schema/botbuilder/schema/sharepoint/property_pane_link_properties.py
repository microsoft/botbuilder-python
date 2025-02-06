# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema.sharepoint.property_pane_field_properties import (
    PropertyPaneFieldProperties,
)
from botbuilder.schema.sharepoint.property_pane_link_popup_window_properties import (
    PropertyPaneLinkPopupWindowProperties,
)


class PropertyPaneLinkProperties(PropertyPaneFieldProperties):
    """
    SharePoint property pane link field properties.

    :param aria_label: The aria label of the link.
    :type aria_label: str
    :param disabled: Indicates whether the link is disabled.
    :type disabled: bool
    :param href: The href of the link.
    :type href: str
    :param popup_window_props: The popup window properties of the link.
    :type popup_window_props: PropertyPaneLinkPopupWindowProperties
    :param target: The target of the link.
    :type target: str
    :param text: The text of the link.
    :type text: str
    """

    # Mapping of class attributes to their serialized keys
    _attribute_map = {
        "aria_label": {"key": "ariaLabel", "type": "str"},
        "disabled": {"key": "disabled", "type": "bool"},
        "href": {"key": "href", "type": "str"},
        "popup_window_props": {
            "key": "popupWindowProps",
            "type": "PropertyPaneLinkPopupWindowProperties",
        },
        "target": {"key": "target", "type": "str"},
        "text": {"key": "text", "type": "str"},
    }

    def __init__(
        self,
        aria_label: str = None,
        disabled: bool = False,
        href: str = None,
        popup_window_props: PropertyPaneLinkPopupWindowProperties = None,
        target: str = None,
        text: str = None,
        **kwargs
    ) -> None:
        super(PropertyPaneLinkProperties, self).__init__(**kwargs)
        self.aria_label = aria_label
        self.disabled = disabled
        self.href = href
        self.popup_window_props = (
            popup_window_props
            if popup_window_props
            else PropertyPaneLinkPopupWindowProperties()
        )
        self.target = target
        self.text = text
