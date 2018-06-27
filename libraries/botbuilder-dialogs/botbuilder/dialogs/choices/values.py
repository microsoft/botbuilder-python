# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class FoundValue:
    def __init__(self, value: str, index: int, score: int = None):
        """INTERNAL: Raw search result returned by `find_values()`.

        :param value:
        :param index:
        :param score:
        """
        self.value = value
        self.index = index
        self.score = score


class SortedValue:
    def __init__(self, value: str, index: int):
        """INTERNAL: A value that can be sorted and still refer to its original position within a source array.

        The `find_choices()` function expands the passed in choices to individual `SortedValue`
        instances and passes them to `find_values()`. Each individual `Choice` can result in multiple
        synonyms that should be searched for so this data structure lets us pass each synonym as a value
        to search while maintaining the index of the choice that value came from.
        :param value:
        :param index:
        """
        """The value that will be sorted."""
        self.value = value

        """The values original position within its unsorted array."""
        self.index = index
