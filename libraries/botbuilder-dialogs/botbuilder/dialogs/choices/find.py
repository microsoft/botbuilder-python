# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict, List, Union

from .tokenizer import Token, Tokenizer
from .model_result import ModelResult
from .choices import Choice, FoundChoice
from .values import SortedValue, FoundValue


class FindChoicesOptions:
    def __init__(self, no_value: bool=False, no_action: bool=False):
        """Options to control the recognition performed by `find_choices()`.
        :param no_value:
        :param no_action:
        """

        """(Optional) If `True`, the choices `value` field will NOT be searched over.
        Defaults to `False`."""
        self.no_value = no_value

        """(Optional) If `True`, the the choices `action.title` field will NOT be searched over. 
        Defaults to `False`."""
        self.no_action = no_action


class FindValuesOptions:
    """
    Basic search options used to control how choices are recognized in a users utterance.
    """
    def __init__(self, allow_partial_matches: bool = False, locale: str = 'en-US', max_token_distance: int = 2,
                 tokenizer=None):
        """

        :param allow_partial_matches:
        :param locale:
        :param max_token_distance:
        :param tokenizer:
        """

        """(Optional) if true, then only some of the tokens in a value need to exist to be considered 
        a match. The default value is "false".
        """
        self.allow_partial_matches = allow_partial_matches

        """(Optional) locale/culture code of the utterance. The default is `en-US`.
        """
        self.locale = locale

        """(Optional) maximum tokens allowed between two matched tokens in the utterance. So with
        a max distance of 2 the value "second last" would match the utterance "second from the last"
        but it wouldn't match "Wait a second. That's not the last one is it?". 
        The default value is "2".  
        """
        self.max_token_distance = max_token_distance

        """(Optional) tokenizer to use when parsing the utterance and values being recognized. """
        self.tokenizer = tokenizer


class Find:
    @staticmethod
    def find_choices(utterance: str,
                     choices: Union[List[str], List[Choice]],
                     options: FindChoicesOptions = FindChoicesOptions()) -> List[ModelResult]:
        """Mid-level search function for recognizing a choice in an utterance.

        This function is layered above `find_values()` and simply determines all of the synonyms that
        should be searched for before calling `find_values()` to perform the actual search. The
        `recognize_choices()` function is layered above this function and adds the ability to select a
        choice by index or ordinal position in the list. Calling this particular function is useful
        when you don't want the index and ordinal position recognition done by `recognize_choices()`.
        :param utterance:
        :param choices:
        :param options:
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def find_values(utterance: str, values: List[SortedValue], options: FindValuesOptions = FindValuesOptions()) -> List[ModelResult]:

        """Sort values in descending order by length so that the longest value is searched over first."""
        list_of_values = sorted(values, key=lambda v: len(v.value), reverse=True)

        matches = []
        opt = options or FindValuesOptions()
        tokenizer = opt.tokenizer or Tokenizer.default_tokenizer
        tokens = tokenizer(utterance, opt.locale)
        max_distance = opt.max_token_distance if opt.max_token_distance else 2

        for index, entry in enumerate(list_of_values):
            """Find all matches for a value.
             - To match "last one" in "the last time I chose the last one" we need 
               to re-search the string starting from the end of the previous match.
             - The start & end position returned for the match are token positions.
            """
            start_pos = 0
            v_tokens = tokenizer(entry.value.strip(), opt.locale)
            while start_pos < len(tokens):
                match = Find._match_value(tokens, entry.index, entry.value, v_tokens, start_pos, max_distance, opt)
                if match:
                    start_pos = match.end + 1
                    matches.append(match)
                else:
                    break

        # Sort matches by score descending.
        matches.sort(key=lambda m: m.resolution.score, reverse=True)
        results = []
        found_indexes: Dict[int, bool] = {}
        used_tokens: Dict[int, bool] = {}
        for match in matches:
            add = match.resolution.index not in found_indexes
            i = match.start
            while i <= match.end:
                if i in used_tokens:
                    add = False

                    break
                i += 1
            # Add to results
            if add:
                found_indexes[match.resolution.index] = True
                idx = match.start
                while idx <= match.end:
                    used_tokens[idx] = True
                    idx += 1

                match.start = tokens[match.start].start
                match.end = tokens[match.end].end
                match.text = utterance[match.start: match.end + 1]
                results.append(match)

        return sorted(results, key=lambda r: r.start)

    @staticmethod
    def _match_value(tokens: List[Token], index: int, value: str, v_tokens: List[Token], start_position: int,
                     max_distance: int, options: FindValuesOptions) -> ModelResult:
        """Match value to utterance and calculate total deviation.
        - The tokens are matched in order so "second last" will match in
          "the second from last one" but not in "the last from the second one".
        - The total deviation is a count of the number of tokens skipped in the
          match so for the example above the number of tokens matched would be
          2 and the total deviation would be 1.
        :param tokens:
        :param index:
        :param value:
        :param v_tokens:
        :param start_position:
        :param max_distance:
        :param options:
        :return:
        """

        matched = 0
        total_deviation = 0
        start = -1
        end = -1

        for token in v_tokens:
            # Find the position of the token in the utterance.
            position = Find._index_of_token(token, start_position, tokens)

            if position >= 0:
                # Calculate the distance between the current tokens position and the previous token's distance.
                distance = position - start_position if matched > 0 else 0
                if distance <= max_distance:
                    matched += 1
                    total_deviation += distance
                    start_position = position + 1

                    if start < 0:
                        start = position
                    end = position

        result: ModelResult = None
        if matched > 0 and (matched == len(v_tokens) or options.allow_partial_matches):
            """Percentage of tokens matched.
            If matching "second last" in  "the second from last one" the completeness would be 1.0 since all 
            tokens were found.
            """
            completeness = matched / len(v_tokens)

            """Accuracy of the match.
            The accuracy is reduced by additional tokens occurring in the value that weren't in the utterance.
            So an utterance of "second last" matched against a value of "second from last" would result in an 
            accuracy of 0.5. 
            """
            accuracy = matched / (matched + total_deviation)

            """The final score is simply the completeness multiplied by the accuracy."""
            score = completeness * accuracy
            result = ModelResult(start=start,
                                 end=end,
                                 type_name='value',
                                 resolution=FoundValue(value=value,
                                                       index=index,
                                                       score=score))
        return result

    @staticmethod
    def _index_of_token(token: Token, start_pos: int, tokens: List[Token]) -> int:
        index = start_pos
        while index < len(tokens):
            if tokens[index].normalized == token.normalized:
                return index
            index += 1
        return -1
