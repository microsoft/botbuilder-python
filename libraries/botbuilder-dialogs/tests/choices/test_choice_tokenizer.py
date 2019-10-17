# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.dialogs.choices import Tokenizer


def _assert_token(token, start, end, text, normalized=None):
    assert (
        token.start == start
    ), f"Invalid token.start of '{token.start}' for '{text}' token."
    assert token.end == end, f"Invalid token.end of '{token.end}' for '{text}' token."
    assert (
        token.text == text
    ), f"Invalid token.text of '{token.text}' for '{text}' token."
    assert (
        token.normalized == normalized or text
    ), f"Invalid token.normalized of '{token.normalized}' for '{text}' token."


class AttachmentPromptTests(aiounittest.AsyncTestCase):
    def test_should_break_on_spaces(self):
        tokens = Tokenizer.default_tokenizer("how now brown cow")
        assert len(tokens) == 4
        _assert_token(tokens[0], 0, 2, "how")
        _assert_token(tokens[1], 4, 6, "now")
        _assert_token(tokens[2], 8, 12, "brown")
        _assert_token(tokens[3], 14, 16, "cow")

    def test_should_break_on_punctuation(self):
        tokens = Tokenizer.default_tokenizer("how-now.brown:cow?")
        assert len(tokens) == 4
        _assert_token(tokens[0], 0, 2, "how")
        _assert_token(tokens[1], 4, 6, "now")
        _assert_token(tokens[2], 8, 12, "brown")
        _assert_token(tokens[3], 14, 16, "cow")

    def test_should_tokenize_single_character_tokens(self):
        tokens = Tokenizer.default_tokenizer("a b c d")
        assert len(tokens) == 4
        _assert_token(tokens[0], 0, 0, "a")
        _assert_token(tokens[1], 2, 2, "b")
        _assert_token(tokens[2], 4, 4, "c")
        _assert_token(tokens[3], 6, 6, "d")

    def test_should_return_a_single_token(self):
        tokens = Tokenizer.default_tokenizer("food")
        assert len(tokens) == 1
        _assert_token(tokens[0], 0, 3, "food")

    def test_should_return_no_tokens(self):
        tokens = Tokenizer.default_tokenizer(".?-()")
        assert not tokens

    def test_should_return_a_the_normalized_and_original_text_for_a_token(self):
        tokens = Tokenizer.default_tokenizer("fOoD")
        assert len(tokens) == 1
        _assert_token(tokens[0], 0, 3, "fOoD", "food")

    def test_should_break_on_emojis(self):
        tokens = Tokenizer.default_tokenizer("food 💥👍😀")
        assert len(tokens) == 4
        _assert_token(tokens[0], 0, 3, "food")
        _assert_token(tokens[1], 5, 5, "💥")
        _assert_token(tokens[2], 6, 6, "👍")
        _assert_token(tokens[3], 7, 7, "😀")
