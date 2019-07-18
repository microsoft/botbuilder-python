# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class Metadata:
    """ Metadata associated with the answer. """

    def __init__(self, name: str, value: str):
        """
        Parameters:
        -----------

        name: Metadata name. Max length: 100.

        value: Metadata value. Max length: 100.
        """
        self.name = name
        self.value = value
