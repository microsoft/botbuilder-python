# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class PropertyPanePageHeader(Model):
    """
    SharePoint property pane page header object.

    :param description: The description of the page header.
    :type description: str
    """

    _attribute_map = {
        "description": {"key": "description", "type": "str"},
    }

    def __init__(self, *, description: str = None, **kwargs) -> None:
        super(PropertyPanePageHeader, self).__init__(**kwargs)
        self.description = description
