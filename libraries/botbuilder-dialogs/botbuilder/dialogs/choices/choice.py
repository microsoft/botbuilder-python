# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.schema import CardAction


class Choice(object):
    def __init__(
        self, value: str = None, action: CardAction = None, synonyms: List[str] = None
    ):
        self._value: str = value
        self._action: CardAction = action
        self._synonyms: List[str] = synonyms

    @property
    def value(self) -> str:
        """Gets the value to return when selected.

        :return: The value to return when selected.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        """Sets the value to return when selected.

        :param value: The value to return when selected.
        :type value: str
        :return:
        :rtype: None
        """
        self._value = value

    @property
    def action(self) -> CardAction:
        """Gets the action to use when rendering the choice as a suggested action or hero card.
        This is optional.

        :return: The action to use when rendering the choice as a suggested action or hero card.
        :rtype: CardAction
        """
        return self._action

    @action.setter
    def action(self, value: CardAction) -> None:
        """Sets the action to use when rendering the choice as a suggested action or hero card.
        This is optional.

        :param value: The action to use when rendering the choice as a suggested action or hero card.
        :type value: CardAction
        :return:
        :rtype: None
        """
        self._action = value

    @property
    def synonyms(self) -> List[str]:
        """Gets the list of synonyms to recognize in addition to the value. This is optional.

        :return: The list of synonyms to recognize in addition to the value.
        :rtype: List[str]
        """
        return self._synonyms

    @synonyms.setter
    def synonyms(self, value: List[str]) -> None:
        """Sets the list of synonyms to recognize in addition to the value. This is optional.

        :param value: The list of synonyms to recognize in addition to the value.
        :type value: List[str]
        :return:
        :rtype: None
        """
        self._synonyms = value
