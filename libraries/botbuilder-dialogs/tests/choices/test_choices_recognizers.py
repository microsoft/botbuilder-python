# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
import unittest
from typing import List

from botbuilder.dialogs.choices import Choice, SortedValue

class ChoiceRecognizersTest(aiounittest.AsyncTestCase):
    # FindChoices

    _color_choices: List[str] = ['red', 'green', 'blue']
    _overlapping_choices: List[str] = ['bread', 'bread pudding', 'pudding']
    
    _color_values: List[SortedValue] = [
        SortedValue(value = 'red', index = 0),
        SortedValue(value = 'green', index = 1),
        SortedValue(value = 'blue', index = 2)
    ]

    _overlapping_values: List[SortedValue] = [
        SortedValue(value = 'bread', index = 0),
        SortedValue(value = 'bread pudding', index = 1),
        SortedValue(value = 'pudding', index = 2)
    ]

    _similar_values: List[SortedValue] = [
        SortedValue(value = 'option A', index = 0),
        SortedValue(value = 'option B', index = 1),
        SortedValue(value = 'option C', index = 2)
    ]

    def test_should_find_a_simple_value_in_a_single_word_utterance(self):
        pass

    def test_should_find_a_simple_value_in_an_utterance(self):
        pass

    def test_should_find_multiple_values_within_an_utterance(self):
        pass

    def test_should_find_multiple_values_that_overlap(self):
        pass
    
    def test_should_correctly_disambiguate_between_similar_values(self):
        pass
    
    def test_should_find_a_single_choice_within_an_utterance(self):
        pass
    
    def test_should_find_multiple_choices_that_overlap(self):
        pass
    
    def test_should_accept_null_utterance_in_find_choices(self):
        pass
    
    def test_should_find_a_choice_in_an_utterance_by_name(self):
        pass
    
    def test_should_find_a_choice_in_an_utterance_by_ordinal_position(self):
        pass