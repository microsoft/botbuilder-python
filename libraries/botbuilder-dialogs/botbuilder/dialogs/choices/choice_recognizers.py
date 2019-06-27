# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List, Union


from .choice import Choice
from .find import Find
from .find_choices_options import FindChoicesOptions
from .found_choice import FoundChoice
from .model_result import ModelResult

class ChoiceRecognizers:
    """ Contains methods for matching user input against a list of choices. """

    @staticmethod
    def recognize_choices(
        utterance: str,
        choices: List[Union[str, Choice]],
        options: FindChoicesOptions = None
    ) -> ModelResult:
        """
        Matches user input against a list of choices.

        This is layered above the `Find.find_choices()` function, and adds logic to let the user specify
        their choice by index (they can say "one to pick `choice[0]`) or ordinal position (they can say "the second one" to pick `choice[1]`.)
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
        if utterance == None:
            utterance = ''

        # Try finding choices by text search first
        # - We only want to use a single strategy for returning results to avoid issues where utterances
        # like the "the third one" or "the red one" or "the first division book" would miss-recognize as
        # a numerical index or ordinal as well
        # TODO complete when recgonizers-numbers is published
        locale = options.locale if options.locale else 'FILL IN WITH RECOGNIZERS-NUMBER (C# Recognizers.Text.Culture.English)'
        matched = Find.find_choices(utterance, choices, options)

        if len(matched) == 0:
            # Next try finding by ordinal
            # matches = WRITE RecognizeOrdinal()
            pass
    
    @staticmethod
    def _recognize_ordinal(utterance: str, culture: str) -> List[ModelResult]:
        # NEED NumberRecognizer class from recognizers-numbers
        pass
        