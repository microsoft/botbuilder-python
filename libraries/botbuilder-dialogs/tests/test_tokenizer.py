# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest
from botbuilder.dialogs.choices import Token, Tokenizer


def assert_token(token: Token, start: int, end: int, text: str, normalized: str = None):
    normalized = normalized if normalized else text
    assert token.start == start, f"Token.start [{token.text}] != start [{start}]"
    assert token.end == end, f"Token.end [{token.end}] != end [{end}]"
    assert token.text == text, f"Token.text [{token.text}] != text [{text}]"
    assert normalized == token.normalized, f"Token.normalized [{token.normalized}] != normalized [{normalized}]"


class TestTokenizer:
    def test_should_break_on_spaces(self):
        tokens = Tokenizer.default_tokenizer('how now brown cow')

        assert len(tokens) == 4
        assert_token(tokens[0], 0, 2, 'how')
        assert_token(tokens[1], 4, 6, 'now')
        assert_token(tokens[2], 8, 12, 'brown')
        assert_token(tokens[3], 14, 16, 'cow')

    def test_should_break_on_punctuation(self):
        tokens = Tokenizer.default_tokenizer('how-now.brown:cow?')

        assert len(tokens) == 4
        assert_token(tokens[0], 0, 2, 'how')
        assert_token(tokens[1], 4, 6, 'now')
        assert_token(tokens[2], 8, 12, 'brown')
        assert_token(tokens[3], 14, 16, 'cow')

    def test_should_tokenize_single_character_tokens(self):
        tokens = Tokenizer.default_tokenizer('a b c d')

        assert len(tokens) == 4
        assert_token(tokens[0], 0, 0, 'a')
        assert_token(tokens[1], 2, 2, 'b')
        assert_token(tokens[2], 4, 4, 'c')
        assert_token(tokens[3], 6, 6, 'd')

    def test_should_return_a_single_token(self):
        tokens = Tokenizer.default_tokenizer('food')

        assert len(tokens) == 1
        assert_token(tokens[0], 0, 3, 'food')

    def test_should_return_no_tokens(self):
        tokens = Tokenizer.default_tokenizer('.?;-()')

        assert len(tokens) == 0

    def test_should_return_the_normalized_and_original_text_for_a_token(self):
        tokens = Tokenizer.default_tokenizer('fOoD')

        assert len(tokens) == 1
        assert_token(tokens[0], 0, 3, 'fOoD', 'food')

    @pytest.mark.skip(reason='Still sorting out Emoji parsing differences and tokenizing in general across SDKs')
    def test_should_break_on_emoji(self):
        tokens = Tokenizer.default_tokenizer("food 🧀👍😀")

        assert len(tokens) == 4
        assert_token(tokens[0], 0, 3, "food")
        assert_token(tokens[1], 5, 6, "🧀")
        assert_token(tokens[2], 7, 8, "👍")
        assert_token(tokens[3], 9, 10, "😀")
