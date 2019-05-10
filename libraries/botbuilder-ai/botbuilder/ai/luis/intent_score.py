# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict


class IntentScore(object):
    """
    Score plus any extra information about an intent.
    """

    def __init__(self, score: float = None, properties: Dict[str, object] = {}):
        self._score: float = score
        self._properties: Dict[str, object] = properties

    @property
    def score(self) -> float:
        """Gets confidence in an intent.
        
        :return: Confidence in an intent.
        :rtype: float
        """

        return self._score

    @score.setter
    def score(self, value: float) -> None:
        """Sets confidence in an intent.
        
        :param value: Confidence in an intent.
        :type value: float
        :return:
        :rtype: None
        """

        self._score = value

    @property
    def properties(self) -> Dict[str, object]:
        """Gets any extra properties to include in the results.
        
        :return: Any extra properties to include in the results.
        :rtype: Dict[str, object]
        """

        return self._properties

    @properties.setter
    def properties(self, value: Dict[str, object]) -> None:
        """Sets any extra properties to include in the results.
        
        :param value: Any extra properties to include in the results.
        :type value: Dict[str, object]
        :return:
        :rtype: None
        """

        self._properties = value
