# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class FoundChoice:
    """Represents a result from matching user input against a list of choices"""

    def __init__(self, value: str, index: int, score: float, synonym: str = None):
        """
        Parameters:
        ----------

        value: The value of the choice that was matched.
        index: The index of the choice within the list of choices that was searched over.

        score: The accuracy with which the synonym matched the specified portion of the utterance.
        A value of 1.0 would indicate a perfect match.

        synonym: (Optional) The synonym that was matched.
        """
        self.value = value
        self.index = index
        self.score = score
        self.synonym = synonym
