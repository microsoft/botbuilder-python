# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import unittest
from typing import List

from botbuilder.dialogs.choices import Choice
from botbuilder.schema import CardAction


class ChoiceTest(unittest.TestCase):
    def test_value_round_trips(self) -> None:
        choice = Choice()
        expected = "any"
        choice.value = expected
        self.assertIs(expected, choice.value)

    def test_action_round_trips(self) -> None:
        choice = Choice()
        expected = CardAction()
        choice.action = expected
        self.assertIs(expected, choice.action)

    def test_synonyms_round_trips(self) -> None:
        choice = Choice()
        expected: List[str] = []
        choice.synonyms = expected
        self.assertIs(expected, choice.synonyms)
