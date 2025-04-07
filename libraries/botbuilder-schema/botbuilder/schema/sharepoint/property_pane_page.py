# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from msrest.serialization import Model

from botbuilder.schema.sharepoint.property_pane_page_header import (
    PropertyPanePageHeader,
)
from botbuilder.schema.sharepoint.property_pane_group_or_conditional_group import (
    PropertyPaneGroupOrConditionalGroup,
)


class PropertyPanePage(Model):
    """
    SharePoint property pane page.

    :param groups: The groups of the page.
    :type groups: list[PropertyPaneGroupOrConditionalGroup]
    :param display_groups_as_accordion: Whether to display the groups as an accordion.
    :type display_groups_as_accordion: bool
    :param header: The header of the page.
    :type header: PropertyPanePageHeader
    """

    _attribute_map = {
        "groups": {"key": "groups", "type": "[PropertyPaneGroupOrConditionalGroup]"},
        "display_groups_as_accordion": {
            "key": "displayGroupsAsAccordion",
            "type": "bool",
        },
        "header": {"key": "header", "type": "PropertyPanePageHeader"},
    }

    def __init__(
        self,
        *,
        groups: List[PropertyPaneGroupOrConditionalGroup] = None,
        display_groups_as_accordion: bool = None,
        header: PropertyPanePageHeader = None,
        **kwargs
    ) -> None:
        super(PropertyPanePage, self).__init__(**kwargs)
        self.groups = groups
        self.display_groups_as_accordion = display_groups_as_accordion
        self.header = header
