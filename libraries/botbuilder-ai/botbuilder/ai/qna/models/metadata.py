# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class Metadata(Model):
    """Metadata associated with the answer."""

    _attribute_map = {
        "name": {"key": "name", "type": "str"},
        "value": {"key": "value", "type": "str"},
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get("name", None)
        self.value = kwargs.get("value", None)
