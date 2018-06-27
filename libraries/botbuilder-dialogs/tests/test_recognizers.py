# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs.choices import ModelResult, SortedValue, Find, FindValuesOptions


def assert_result(result: ModelResult, start: int, end: int, text: str):
    assert result.start == start, f"ModelResult.start [{result.start}] != start [{start}]"
    assert result.end == end, f"ModelResult.end [{result.end}] != end [{end}]"
    assert result.text == text, f"ModelResult.text [{result.text}] != text [{text}]"


def assert_value(result: ModelResult, value: str, index, score):
    assert result.type_name == 'value', f"Invalid ModelResult.type_name for '{result.type_name}' for '{value}' value/"
    assert result.resolution is not None, f"Missing ModelResult.resolution for '{value}' value."
    resolution = result.resolution
    assert resolution.value == value, f"Invalid resolution.value of '{resolution.index}' for '${value}' value."
    assert resolution.index == index, f"Invalid resolution.index of '{resolution.index}' for '${value}' value."
    assert resolution.score == score, f"Invalid resolution.score of '{resolution.score}' for '{value}' value."


def assert_choice(result: ModelResult, value: str, index: int, score: float, synonym: str = None):
    assert result.type_name == 'choice', f"Invalid ModelResult.type_name for '{result.type_name}' for '{value}' choice/"
    assert result.resolution is not None, f"Missing ModelResult.resolution for '{value}' choice."
    resolution = result.resolution
    assert resolution.value == value, f"Invalid resolution.value of '{resolution.index}' for '${value}' choice."
    assert resolution.index == index, f"Invalid resolution.index of '{resolution.index}' for '${value}' choice."
    assert resolution.score == score, f"Invalid resolution.score of '{resolution.score}' for '{value}' choice."
    if synonym is not None:
        assert resolution.synonym == synonym, (f"Invalid resolution.synonym of '{resolution.synonym}' for '{value}'"
                                               f" choice.")


"""find_values() tests"""


COLOR_VALUES = [
    SortedValue(value='red', index=0),
    SortedValue(value='green', index=1),
    SortedValue(value='blue', index=2)
]


OVERLAPPING_VALUES = [
    SortedValue(value='bread', index=0),
    SortedValue(value='bread pudding', index=1),
    SortedValue(value='pudding', index=2)
]

SIMILAR_VALUES = [
    SortedValue(value='option A', index=0),
    SortedValue(value='option B', index=1),
    SortedValue(value='option C', index=2)
]


class TestFindValues:
    def test_should_find_a_simple_value_in_a_single_world_utterance(self):
        found = Find.find_values('red', COLOR_VALUES)
        assert len(found) == 1, f"Invalid token count of '{len(found)}' returned."
        assert_result(found[0], 0, 2, 'red')
        assert_value(found[0], 'red', 0, 1.0)

    def test_should_find_a_value_in_an_utterance(self):
        found = Find.find_values('the red one please.', COLOR_VALUES)  # the red one please
        assert len(found) == 1, f"Invalid token count of '{len(found)}' returned."
        assert_result(found[0], 4, 6, 'red')
        assert_value(found[0], 'red', 0, 1.0)

    def test_should_find_multiple_values_within_an_utterance(self):
        found = Find.find_values('the red and blue ones please.', COLOR_VALUES)
        assert len(found) == 2, f"Invalid token count of '{len(found)}' returned."
        assert_result(found[0], 4, 6, 'red')
        assert_value(found[0], 'red', 0, 1.0)
        assert_value(found[1], 'blue', 2, 1.0)

    def test_should_find_multiple_values_that_overlap(self):
        found = Find.find_values('the bread pudding and bread please.', OVERLAPPING_VALUES)
        assert len(found) == 2, f"Invalid token count of '{len(found)}' returned."

        for f in found:
            print(f"f.text: {f.text}, f.start: {f.start}")

        assert_result(found[0], 4, 16, 'bread pudding')
        assert_value(found[0], 'bread pudding', 1, 1.0)
        assert_value(found[1], 'bread', 0, 1.0)

    def test_should_correctly_disambiguate_between_very_similar_values(self):
        found = Find.find_values('option B', SIMILAR_VALUES, FindValuesOptions(allow_partial_matches=True))
        assert len(found) == 1, f"Invalid token count of '{len(found)}' returned."
        assert_value(found[0], 'option B', 1, 1.0)
