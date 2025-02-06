# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class QuickViewData(Model):
    """
    SharePoint Quick View Data.

    :param title: The title of the quick view data.
    :type title: str
    :param description: The description of the quick view data.
    :type description: str
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "description": {"key": "description", "type": "str"},
    }

    def __init__(self, *, title: str = None, description: str = None, **kwargs) -> None:
        super(QuickViewData, self).__init__(**kwargs)
        self.title = title
        self.description = description
