# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Callable, List, Union

from .choice import Choice
from .find_choices_options import FindChoicesOptions, FindValuesOptions
from .model_result import ModelResult
from .sorted_value import SortedValue
from .token import Token

class Find:
    """ Contains methods for matching user input against a list of choices """
    
    @staticmethod
    def find_choices(
        utterance: str,
        choices: [ Union[str, Choice] ],
        options: FindChoicesOptions = None
    ):
        """ Matches user input against a list of choices """

        if not choices:
            raise TypeError('Find: choices cannot be None. Must be a [str] or [Choice].')
        
        opt = options if options else FindChoicesOptions()

        # Normalize list of choices
        choices_list = [ Choice(value=choice) if isinstance(choice, str) else choice for choice in choices ]

        # Build up full list of synonyms to search over.
        # - Each entry in the list contains the index of the choice it belongs to which will later be
        # used to map the search results back to their choice.
        synonyms: [SortedValue] = []

        for index in range(len(choices_list)):
            choice = choices_list[index]

            if not opt.no_value:
                synonyms.append( SortedValue(value=choice.value, index=index) )
            
            if getattr(choice, 'action', False) and getattr(choice.action, 'title', False) and not opt.no_value:
                synonyms.append( SortedValue(value=choice.action.title, index=index) )
            
            if choice.synonyms != None:
                for synonym in synonyms:
                    synonyms.append( SortedValue(value=synonym, index=index) )
        
        # Find synonyms in utterance and map back to their choices_list
        # WRITE FindValues()!!
    
    @staticmethod
    def _find_values(
        utterance: str,
        values: List[SortedValue],
        options: FindValuesOptions = None
    ):
        # Sort values in descending order by length, so that the longest value is searchd over first.
        sorted_values = sorted(
            values,
            key = lambda sorted_val: len(sorted_val.value),
            reverse = True
        )

        # Search for each value within the utterance.
        matches: [ModelResult] = []
        opt = options if options else FindValuesOptions()
        # tokenizer: Callable[[str, str], List[Token]] = opt.tokenizer if opt.tokenizer else 