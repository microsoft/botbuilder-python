# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class SortedValue:
    """A value that can be sorted and still refer to its original position with a source array."""

    def __init__(self, value: str, index: int):
        """
        Parameters:
        -----------

        value: The value that will be sorted.

        index: The values original position within its unsorted array.
        """

        self.value = value
        self.index = index
