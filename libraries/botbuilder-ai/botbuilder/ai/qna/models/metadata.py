# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class Metadata(Model):
    """ Metadata associated with the answer. """

    _attribute_map = {
        "name": {"key": "name", "type": "str"},
        "value": {"key": "value", "type": "str"},
    }

    def __init__(self, name: str, value: str, **kwargs):
        """
        Parameters:
        -----------

        name: Metadata name. Max length: 100.

        value: Metadata value. Max length: 100.
        """

        super().__init__(**kwargs)

        self.name = name
        self.value = value
