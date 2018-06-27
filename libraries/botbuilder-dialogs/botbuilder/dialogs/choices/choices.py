# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from botbuilder.schema import CardAction


class Choice:
    def __init__(self, value: str, action: CardAction = None, synonyms: List[str] = None):
        """An instance of a choice that can be used to render a choice to a user or recognize something a
        user picked.
        :param value:
        :param action:
        :param synonyms:
        """

        """Value to return when recognized by "find_choices()".
        Will also be used to render choices to the user if no action is provided."""
        self.value = value

        """(Optional) action to use when rendering the choice as a suggested action. This **MUST**
        be a complete action containing `type`, `title`, and `value` fields. If not specified an
        `imBack` action will be generated based on the choices value field. """
        self.action = action

        """(Optional) list of synonyms to recognize in addition to the value and 
        action fields."""
        self.synonyms = synonyms


class FoundChoice:
    def __init__(self, value: str, index: int, score: float, synonym: str=None):
        """Result returned by `find_choices()`.
        :param value:
        :param index:
        :param score:
        :param synonym:
        """

        """The value of the choice that was matched."""
        self.value = value

        """The choices index within the list of choices that was searched over."""
        self.index = index

        """The accuracy with which the synonym matched the specified portion of the utterance.
        A value of 1.0 would indicate a perfect match."""
        self.score = score

        """(Optional) The synonym that was matched."""
        self.synonym = synonym
