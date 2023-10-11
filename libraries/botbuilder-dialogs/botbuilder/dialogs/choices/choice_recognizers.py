# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List, Union
from recognizers_number import NumberModel, NumberRecognizer, OrdinalModel
from recognizers_text import Culture


from .choice import Choice
from .find import Find
from .find_choices_options import FindChoicesOptions
from .found_choice import FoundChoice
from .model_result import ModelResult


class ChoiceRecognizers:
    """Contains methods for matching user input against a list of choices."""

    @staticmethod
    def recognize_choices(
        utterance: str,
        choices: List[Union[str, Choice]],
        options: FindChoicesOptions = None,
    ) -> List[ModelResult]:
        """
        Matches user input against a list of choices.

        This is layered above the `Find.find_choices()` function, and adds logic to let the user specify
        their choice by index (they can say "one" to pick `choice[0]`) or ordinal position
         (they can say "the second one" to pick `choice[1]`.)
        The user's utterance is recognized in the following order:

        - By name using `find_choices()`
        - By 1's based ordinal position.
        - By 1's based index position.

        Parameters:
        -----------

        utterance: The input.

        choices: The list of choices.

        options: (Optional) Options to control the recognition strategy.

        Returns:
        --------
        A list of found choices, sorted by most relevant first.
        """
        if utterance is None:
            utterance = ""

        # Normalize list of choices
        choices_list = [
            Choice(value=choice) if isinstance(choice, str) else choice
            for choice in choices
        ]

        # Try finding choices by text search first
        # - We only want to use a single strategy for returning results to avoid issues where utterances
        #   like the "the third one" or "the red one" or "the first division book" would miss-recognize as
        #   a numerical index or ordinal as well.
        locale = options.locale if (options and options.locale) else Culture.English
        matched = Find.find_choices(utterance, choices_list, options)
        if not matched:
            matches = []

            if not options or options.recognize_ordinals:
                # Next try finding by ordinal
                matches = ChoiceRecognizers._recognize_ordinal(utterance, locale)
                for match in matches:
                    ChoiceRecognizers._match_choice_by_index(
                        choices_list, matched, match
                    )

            if not matches and (not options or options.recognize_numbers):
                # Then try by numerical index
                matches = ChoiceRecognizers._recognize_number(utterance, locale)
                for match in matches:
                    ChoiceRecognizers._match_choice_by_index(
                        choices_list, matched, match
                    )

            # Sort any found matches by their position within the utterance.
            # - The results from find_choices() are already properly sorted so we just need this
            #   for ordinal & numerical lookups.
            matched = sorted(matched, key=lambda model_result: model_result.start)

        return matched

    @staticmethod
    def _recognize_ordinal(utterance: str, culture: str) -> List[ModelResult]:
        model: OrdinalModel = NumberRecognizer(culture).get_ordinal_model(culture)

        return list(
            map(ChoiceRecognizers._found_choice_constructor, model.parse(utterance))
        )

    @staticmethod
    def _match_choice_by_index(
        choices: List[Choice], matched: List[ModelResult], match: ModelResult
    ):
        try:
            index: int = int(match.resolution.value) - 1
            if 0 <= index < len(choices):
                choice = choices[index]

                matched.append(
                    ModelResult(
                        start=match.start,
                        end=match.end,
                        type_name="choice",
                        text=match.text,
                        resolution=FoundChoice(
                            value=choice.value, index=index, score=1.0
                        ),
                    )
                )
        except:
            # noop here, as in dotnet/node repos
            pass

    @staticmethod
    def _recognize_number(utterance: str, culture: str) -> List[ModelResult]:
        model: NumberModel = NumberRecognizer(culture).get_number_model(culture)

        return list(
            map(ChoiceRecognizers._found_choice_constructor, model.parse(utterance))
        )

    @staticmethod
    def _found_choice_constructor(value_model: ModelResult) -> ModelResult:
        return ModelResult(
            start=value_model.start,
            end=value_model.end,
            type_name="choice",
            text=value_model.text,
            resolution=FoundChoice(
                value=value_model.resolution["value"], index=0, score=1.0
            ),
        )
