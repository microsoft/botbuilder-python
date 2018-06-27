# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Any


class ModelResult:
    def __init__(self, text: str = None, start: int = None, end: int = None, type_name: str = None,
                 resolution: Any = None):
        """Outer result returned by an entity recognizer like 'recognize_choices()'.

        This structure is wrapped around the recognized result and contains start and
        end position information to identify the span of text in the users utterance that was
        recognized. The actual result can be accessed through the resolution property.
        :param text:
        :param start:
        :param end:
        :param type_name:
        :param resolution:
        """

        """Substring of the utterance that was recognized."""
        self.text = text

        """Start character position of the recognized substring."""
        self.start = start

        """End character position of the recognized substring."""
        self.end = end

        """Type of entity that was recognized."""
        self.type_name = type_name

        """The recognized entity."""
        self.resolution = resolution
