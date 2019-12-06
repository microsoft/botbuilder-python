# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Callable, List, Union

from .choice import Choice
from .find_choices_options import FindChoicesOptions, FindValuesOptions
from .found_choice import FoundChoice
from .found_value import FoundValue
from .model_result import ModelResult
from .sorted_value import SortedValue
from .token import Token
from .tokenizer import Tokenizer


class Find:
    """ Contains methods for matching user input against a list of choices """

    @staticmethod
    def find_choices(
        utterance: str,
        choices: [Union[str, Choice]],
        options: FindChoicesOptions = None,
    ):
        """ Matches user input against a list of choices """

        if not choices:
            raise TypeError(
                "Find: choices cannot be None. Must be a [str] or [Choice]."
            )

        opt = options if options else FindChoicesOptions()

        # Normalize list of choices
        choices_list = [
            Choice(value=choice) if isinstance(choice, str) else choice
            for choice in choices
        ]

        # Build up full list of synonyms to search over.
        # - Each entry in the list contains the index of the choice it belongs to which will later be
        # used to map the search results back to their choice.
        synonyms: [SortedValue] = []

        for index, choice in enumerate(choices_list):
            if not opt.no_value:
                synonyms.append(SortedValue(value=choice.value, index=index))

            if (
                getattr(choice, "action", False)
                and getattr(choice.action, "title", False)
                and not opt.no_value
            ):
                synonyms.append(SortedValue(value=choice.action.title, index=index))

            if choice.synonyms is not None:
                for synonym in choice.synonyms:
                    synonyms.append(SortedValue(value=synonym, index=index))

        def found_choice_constructor(value_model: ModelResult) -> ModelResult:
            choice = choices_list[value_model.resolution.index]

            return ModelResult(
                start=value_model.start,
                end=value_model.end,
                type_name="choice",
                text=value_model.text,
                resolution=FoundChoice(
                    value=choice.value,
                    index=value_model.resolution.index,
                    score=value_model.resolution.score,
                    synonym=value_model.resolution.value,
                ),
            )

        # Find synonyms in utterance and map back to their choices_list
        return list(
            map(
                found_choice_constructor, Find.find_values(utterance, synonyms, options)
            )
        )

    @staticmethod
    def find_values(
        utterance: str, values: List[SortedValue], options: FindValuesOptions = None
    ) -> List[ModelResult]:
        # Sort values in descending order by length, so that the longest value is searchd over first.
        sorted_values = sorted(
            values, key=lambda sorted_val: len(sorted_val.value), reverse=True
        )

        # Search for each value within the utterance.
        matches: [ModelResult] = []
        opt = options if options else FindValuesOptions()
        tokenizer: Callable[
            [str, str], List[Token]
        ] = opt.tokenizer if opt.tokenizer else Tokenizer.default_tokenizer
        tokens = tokenizer(utterance, opt.locale)
        max_distance = (
            opt.max_token_distance if opt.max_token_distance is not None else 2
        )

        for entry in sorted_values:

            # Find all matches for a value
            # - To match "last one" in "the last time I chose the last one" we need
            #   to re-search the string starting from the end of the previous match.
            # - The start & end position returned for the match are token positions.
            start_pos = 0
            searched_tokens = tokenizer(entry.value.strip(), opt.locale)

            while start_pos < len(tokens):
                match: Union[ModelResult, None] = Find._match_value(
                    tokens,
                    max_distance,
                    opt,
                    entry.index,
                    entry.value,
                    searched_tokens,
                    start_pos,
                )

                if match is not None:
                    start_pos = match.end + 1
                    matches.append(match)
                else:
                    break

        # Sort matches by score descending
        sorted_matches = sorted(
            matches,
            key=lambda model_result: model_result.resolution.score,
            reverse=True,
        )

        # Filter out duplicate matching indexes and overlapping characters
        # - The start & end positions are token positions and need to be translated to
        # character positions before returning. We also need to populate the "text"
        # field as well.
        results: List[ModelResult] = []
        found_indexes = set()
        used_tokens = set()

        for match in sorted_matches:
            # Apply filters.
            add = match.resolution.index not in found_indexes

            for i in range(match.start, match.end + 1):
                if i in used_tokens:
                    add = False
                    break

            # Add to results
            if add:
                # Update filter info
                found_indexes.add(match.resolution.index)

                for i in range(match.start, match.end + 1):
                    used_tokens.add(i)

                # Translate start & end and populate text field
                match.start = tokens[match.start].start
                match.end = tokens[match.end].end
                match.text = utterance[match.start : match.end + 1]
                results.append(match)

        # Return the results sorted by position in the utterance
        return sorted(results, key=lambda model_result: model_result.start)

    @staticmethod
    def _match_value(
        source_tokens: List[Token],
        max_distance: int,
        options: FindValuesOptions,
        index: int,
        value: str,
        searched_tokens: List[Token],
        start_pos: int,
    ) -> Union[ModelResult, None]:
        # Match value to utterance and calculate total deviation.
        # - The tokens are matched in order so "second last" will match in
        #   "the second from last one" but not in "the last from the second one".
        # - The total deviation is a count of the number of tokens skipped in the
        #   match so for the example above the number of tokens matched would be
        #   2 and the total deviation would be 1.
        matched = 0
        total_deviation = 0
        start = -1
        end = -1

        for token in searched_tokens:
            # Find the position of the token in the utterance.
            pos = Find._index_of_token(source_tokens, token, start_pos)
            if pos >= 0:
                # Calculate the distance between the current token's position and the previous token's distance.
                distance = pos - start_pos if matched > 0 else 0
                if distance <= max_distance:
                    # Update count of tokens matched and move start pointer to search for next token
                    # after the current token
                    matched += 1
                    total_deviation += distance
                    start_pos = pos + 1

                    # Update start & end position that will track the span of the utterance that's matched.
                    if start < 0:
                        start = pos

                    end = pos

        # Calculate score and format result
        # - The start & end positions and the results text field will be corrected by the caller.
        result: ModelResult = None

        if matched > 0 and (
            matched == len(searched_tokens) or options.allow_partial_matches
        ):
            # Percentage of tokens matched. If matching "second last" in
            # "the second form last one" the completeness would be 1.0 since
            # all tokens were found.
            completeness = matched / len(searched_tokens)

            # Accuracy of the match. The accuracy is reduced by additional tokens
            # occuring in the value that weren't in the utterance. So an utterance
            # of "second last" matched against a value of "second from last" would
            # result in an accuracy of 0.5.
            accuracy = float(matched) / (matched + total_deviation)

            # The final score is simply the compeleteness multiplied by the accuracy.
            score = completeness * accuracy

            # Format result
            result = ModelResult(
                text="",
                start=start,
                end=end,
                type_name="value",
                resolution=FoundValue(value=value, index=index, score=score),
            )

        return result

    @staticmethod
    def _index_of_token(tokens: List[Token], token: Token, start_pos: int) -> int:
        for i in range(start_pos, len(tokens)):
            if tokens[i].normalized == token.normalized:
                return i

        return -1
