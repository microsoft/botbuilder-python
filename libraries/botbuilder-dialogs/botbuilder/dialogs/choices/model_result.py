# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class ModelResult:
    """Contains recognition result information."""

    def __init__(
        self, text: str, start: int, end: int, type_name: str, resolution: object
    ):
        """
        Parameters:
        ----------

        text: Substring of the utterance that was recognized.

        start: Start character position of the recognized substring.

        end: The end character position of the recognized substring.

        type_name: The type of the entity that was recognized.

        resolution: The recognized entity object.
        """
        self.text = text
        self.start = start
        self.end = end
        self.type_name = type_name
        self.resolution = resolution
