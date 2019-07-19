# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import List

import aiounittest

from botbuilder.dialogs.choices import (
    ChoiceRecognizers,
    Find,
    FindValuesOptions,
    SortedValue,
)


def assert_result(result, start, end, text):
    assert (
        result.start == start
    ), f"Invalid ModelResult.start of '{result.start}' for '{text}' result."
    assert (
        result.end == end
    ), f"Invalid ModelResult.end of '{result.end}' for '{text}' result."
    assert (
        result.text == text
    ), f"Invalid ModelResult.text of '{result.text}' for '{text}' result."


def assert_value(result, value, index, score):
    assert (
        result.type_name == "value"
    ), f"Invalid ModelResult.type_name of '{result.type_name}' for '{value}' value."
    assert result.resolution, f"Missing ModelResult.resolution for '{value}' value."
    resolution = result.resolution
    assert (
        resolution.value == value
    ), f"Invalid resolution.value of '{resolution.value}' for '{value}' value."
    assert (
        resolution.index == index
    ), f"Invalid resolution.index of '{resolution.index}' for '{value}' value."
    assert (
        resolution.score == score
    ), f"Invalid resolution.score of '{resolution.score}' for '{value}' value."


def assert_choice(result, value, index, score, synonym=None):
    assert (
        result.type_name == "choice"
    ), f"Invalid ModelResult.type_name of '{result.type_name}' for '{value}' choice."
    assert result.resolution, f"Missing ModelResult.resolution for '{value}' choice."
    resolution = result.resolution
    assert (
        resolution.value == value
    ), f"Invalid resolution.value of '{resolution.value}' for '{value}' choice."
    assert (
        resolution.index == index
    ), f"Invalid resolution.index of '{resolution.index}' for '{value}' choice."
    assert (
        resolution.score == score
    ), f"Invalid resolution.score of '{resolution.score}' for '{value}' choice."
    if synonym:
        assert (  # pylint: disable=assert-on-tuple
            resolution.synonym == synonym,
            f"Invalid resolution.synonym of '{resolution.synonym}' for '{value}' choice.",
        )


_color_choices: List[str] = ["red", "green", "blue"]
_overlapping_choices: List[str] = ["bread", "bread pudding", "pudding"]

_color_values: List[SortedValue] = [
    SortedValue(value="red", index=0),
    SortedValue(value="green", index=1),
    SortedValue(value="blue", index=2),
]

_overlapping_values: List[SortedValue] = [
    SortedValue(value="bread", index=0),
    SortedValue(value="bread pudding", index=1),
    SortedValue(value="pudding", index=2),
]

_similar_values: List[SortedValue] = [
    SortedValue(value="option A", index=0),
    SortedValue(value="option B", index=1),
    SortedValue(value="option C", index=2),
]


class ChoiceRecognizersTest(aiounittest.AsyncTestCase):
    # Find.find_values

    def test_should_find_a_simple_value_in_a_single_word_utterance(self):
        found = Find.find_values("red", _color_values)
        assert len(found) == 1, f"Invalid token count of '{len(found)}' returned."
        assert_result(found[0], 0, 2, "red")
        assert_value(found[0], "red", 0, 1.0)

    def test_should_find_a_simple_value_in_an_utterance(self):
        found = Find.find_values("the red one please.", _color_values)
        assert len(found) == 1, f"Invalid token count of '{len(found)}' returned."
        assert_result(found[0], 4, 6, "red")
        assert_value(found[0], "red", 0, 1.0)

    def test_should_find_multiple_values_within_an_utterance(self):
        found = Find.find_values("the red and blue ones please.", _color_values)
        assert len(found) == 2, f"Invalid token count of '{len(found)}' returned."
        assert_result(found[0], 4, 6, "red")
        assert_value(found[0], "red", 0, 1.0)
        assert_value(found[1], "blue", 2, 1.0)

    def test_should_find_multiple_values_that_overlap(self):
        found = Find.find_values(
            "the bread pudding and bread please.", _overlapping_values
        )
        assert len(found) == 2, f"Invalid token count of '{len(found)}' returned."
        assert_result(found[0], 4, 16, "bread pudding")
        assert_value(found[0], "bread pudding", 1, 1.0)
        assert_value(found[1], "bread", 0, 1.0)

    def test_should_correctly_disambiguate_between_similar_values(self):
        found = Find.find_values(
            "option B", _similar_values, FindValuesOptions(allow_partial_matches=True)
        )
        assert len(found) == 1, f"Invalid token count of '{len(found)}' returned."
        assert_value(found[0], "option B", 1, 1.0)

    def test_should_find_a_single_choice_in_an_utterance(self):
        found = Find.find_choices("the red one please.", _color_choices)
        assert len(found) == 1, f"Invalid token count of '{len(found)}' returned."
        assert_result(found[0], 4, 6, "red")
        assert_choice(found[0], "red", 0, 1.0, "red")

    def test_should_find_multiple_choices_within_an_utterance(self):
        found = Find.find_choices("the red and blue ones please.", _color_choices)
        assert len(found) == 2, f"Invalid token count of '{len(found)}' returned."
        assert_result(found[0], 4, 6, "red")
        assert_choice(found[0], "red", 0, 1.0)
        assert_choice(found[1], "blue", 2, 1.0)

    def test_should_find_multiple_choices_that_overlap(self):
        found = Find.find_choices(
            "the bread pudding and bread please.", _overlapping_choices
        )
        assert len(found) == 2, f"Invalid token count of '{len(found)}' returned."
        assert_result(found[0], 4, 16, "bread pudding")
        assert_choice(found[0], "bread pudding", 1, 1.0)
        assert_choice(found[1], "bread", 0, 1.0)

    def test_should_accept_null_utterance_in_find_choices(self):
        found = Find.find_choices(None, _color_choices)
        assert not found

    # ChoiceRecognizers.recognize_choices

    def test_should_find_a_choice_in_an_utterance_by_name(self):
        found = ChoiceRecognizers.recognize_choices(
            "the red one please.", _color_choices
        )
        assert len(found) == 1
        assert_result(found[0], 4, 6, "red")
        assert_choice(found[0], "red", 0, 1.0, "red")

    def test_should_find_a_choice_in_an_utterance_by_ordinal_position(self):
        found = ChoiceRecognizers.recognize_choices(
            "the first one please.", _color_choices
        )
        assert len(found) == 1
        assert_result(found[0], 4, 8, "first")
        assert_choice(found[0], "red", 0, 1.0)

    def test_should_find_multiple_choices_in_an_utterance_by_ordinal_position(self):
        found = ChoiceRecognizers.recognize_choices(
            "the first and third one please", _color_choices
        )
        assert len(found) == 2
        assert_choice(found[0], "red", 0, 1.0)
        assert_choice(found[1], "blue", 2, 1.0)

    def test_should_find_a_choice_in_an_utterance_by_numerical_index_digit(self):
        found = ChoiceRecognizers.recognize_choices("1", _color_choices)
        assert len(found) == 1
        assert_result(found[0], 0, 0, "1")
        assert_choice(found[0], "red", 0, 1.0)

    def test_should_find_a_choice_in_an_utterance_by_numerical_index_text(self):
        found = ChoiceRecognizers.recognize_choices("one", _color_choices)
        assert len(found) == 1
        assert_result(found[0], 0, 2, "one")
        assert_choice(found[0], "red", 0, 1.0)

    def test_should_find_multiple_choices_in_an_utterance_by_numerical_index(self):
        found = ChoiceRecognizers.recognize_choices("option one and 3.", _color_choices)
        assert len(found) == 2
        assert_choice(found[0], "red", 0, 1.0)
        assert_choice(found[1], "blue", 2, 1.0)

    def test_should_accept_null_utterance_in_recognize_choices(self):
        found = ChoiceRecognizers.recognize_choices(None, _color_choices)
        assert not found
