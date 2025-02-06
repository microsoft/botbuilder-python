# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from botbuilder.schema.sharepoint.property_pane_group_field import (
    PropertyPaneGroupField,
)
from botbuilder.schema.sharepoint.property_pane_group_or_conditional_group import (
    PropertyPaneGroupOrConditionalGroup,
)


class PropertyPaneGroup(PropertyPaneGroupOrConditionalGroup):
    """
    SharePoint property pane group object.

    :param is_expanded: Indicates whether the group is expanded.
    :type is_expanded: bool
    :param group_fields: The fields of the group.
    :type group_fields: list[PropertyPaneFieldProperties]
    """

    _attribute_map = {
        "group_fields": {"key": "groupFields", "type": "[PropertyPaneFieldProperties]"},
        "group_name": {"key": "groupName", "type": "str"},
        "is_collapsed": {"key": "isCollapsed", "type": "bool"},
        "is_group_name_hidden": {"key": "isGroupNameHidden", "type": "bool"},
    }

    def __init__(
        self,
        *,
        group_fields: List["PropertyPaneGroupField"] = None,
        group_name: str = "",
        is_collapsed: bool = False,
        is_group_name_hidden: bool = False,
        **kwargs
    ) -> None:
        super(PropertyPaneGroup, self).__init__(**kwargs)
        self.group_fields = group_fields
        self.group_name = group_name
        self.is_collapsed = is_collapsed
        self.is_group_name_hidden = is_group_name_hidden
