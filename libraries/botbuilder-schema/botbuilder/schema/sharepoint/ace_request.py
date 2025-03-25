# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class AceRequest(Model):
    """
    SharePoint Ace Request object.

    :param data: The data of the request.
    :type data: object
    :param properties: The properties of the card.
    :type properties: object
    """

    _attribute_map = {
        "data": {"key": "data", "type": "object"},
        "properties": {"key": "properties", "type": "object"},
    }

    def __init__(
        self, *, data: object = None, properties: object = None, **kwargs
    ) -> None:
        super(AceRequest, self).__init__(**kwargs)
        self.data = data
        self.properties = properties
