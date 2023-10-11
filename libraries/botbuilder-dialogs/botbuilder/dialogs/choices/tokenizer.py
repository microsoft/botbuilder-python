# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Union

from .token import Token


class Tokenizer:
    """Provides a default tokenizer implementation."""

    @staticmethod
    def default_tokenizer(  # pylint: disable=unused-argument
        text: str, locale: str = None
    ) -> [Token]:
        """
        Simple tokenizer that breaks on spaces and punctuation. The only normalization is to lowercase.

        Parameter:
        ---------

        text: The input text.

        locale: (Optional) Identifies the locale of the input text.
        """
        tokens: [Token] = []
        token: Union[Token, None] = None

        # Parse text
        length: int = len(text) if text else 0
        i: int = 0

        while i < length:
            # Get both the UNICODE value of the current character and the complete character itself
            # which can potentially be multiple segments
            code_point = ord(text[i])
            char = chr(code_point)

            # Process current character
            if Tokenizer._is_breaking_char(code_point):
                # Character is in Unicode Plane 0 and is in an excluded block
                Tokenizer._append_token(tokens, token, i - 1)
                token = None
            elif code_point > 0xFFFF:
                # Character is in a Supplementary Unicode Plane. This is where emoji live so
                # we're going to just break each character in this range out as its own token
                Tokenizer._append_token(tokens, token, i - 1)
                token = None
                tokens.append(Token(start=i, end=i, text=char, normalized=char))
            elif token is None:
                # Start a new token
                token = Token(start=i, end=0, text=char, normalized=None)
            else:
                # Add onto current token
                token.text += char

            i += 1

        Tokenizer._append_token(tokens, token, length - 1)

        return tokens

    @staticmethod
    def _is_breaking_char(code_point) -> bool:
        return (
            Tokenizer._is_between(code_point, 0x0000, 0x002F)
            or Tokenizer._is_between(code_point, 0x003A, 0x0040)
            or Tokenizer._is_between(code_point, 0x005B, 0x0060)
            or Tokenizer._is_between(code_point, 0x007B, 0x00BF)
            or Tokenizer._is_between(code_point, 0x02B9, 0x036F)
            or Tokenizer._is_between(code_point, 0x2000, 0x2BFF)
            or Tokenizer._is_between(code_point, 0x2E00, 0x2E7F)
        )

    @staticmethod
    def _is_between(value: int, from_val: int, to_val: int) -> bool:
        """
        Parameters:
        -----------

        value: number value

        from: low range

        to: high range
        """
        return from_val <= value <= to_val

    @staticmethod
    def _append_token(tokens: [Token], token: Token, end: int):
        if token is not None:
            token.end = end
            token.normalized = token.text.lower()
            tokens.append(token)
