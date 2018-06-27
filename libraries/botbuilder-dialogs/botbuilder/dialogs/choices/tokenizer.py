# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Callable, List


class Token:
    def __init__(self, start: int, text: str, end: int = None, normalized: str = None):
        """Individual token returned by a `TokenizerFunction`.
        :param start:
        :param text:
        :param end:
        :param normalized:
        """

        """Start character position of the token within the outer string."""
        self.start = start

        """End character position of the token within the outer string."""
        self.end = end

        """Original text of the token."""
        self.text = text

        """Normalized form of the token. This can include things like lower casing or stemming."""
        self.normalized = normalized


"""Signature for an alternate word breaker that can be passed to `recognize_choices()`, `find_choices()`, or 
`find_values()`. """
TokenizerFunction = Callable[[str, str], List[Token]]


class Tokenizer:
    @staticmethod
    def default_tokenizer(text: str, locale: str = None) -> List[Token]:
        """Simple tokenizer that breaks on spaces and punctuation.

        The only normalization done is to lowercase. This is an exact port of the JavaScript implementation of the
        algorithm. However, due to differences between Python and JavaScript the actual functionality differs. Python
        considers Emoji (and other characters or graphemes) that are surrogate pairs to have a length of 1, whereas
        JavaScript will return a length of 2.
        :param text:
        :param locale:
        :return:
        """
        tokens = []
        token = None

        # Prepare to parse text
        length = len(text) if type(text) == str else 0
        i = 0

        while i < length:
            # Get both the UNICODE value of the current character and the complete character itself
            # which can potentially be multiple segments.
            code_point = ord(text[i])
            char = chr(code_point)

            # Process current character
            if Tokenizer.__is_breaking_char(code_point):
                # Character is in Unicode Plane 0 and is in an excluded block
                Tokenizer.__append_token(tokens, token, i - 1)
                token = None

            elif code_point > 0xFFFF:
                # Character is in a Supplementary Unicode Plane. This is where emoji live so
                # we're going to just break each character in this range out as its own token.
                Tokenizer.__append_token(tokens, token, i - 1)
                token = None
                tokens.append(Token(start=i,
                                    end=(i + len(char) - 1),
                                    text=char,
                                    normalized=char.lower()))

            elif not token:
                # Start a new token
                token = Token(start=i, text=char)
            else:
                # Add on to current token
                token.text += char
            i += len(char)
        Tokenizer.__append_token(tokens, token, length - 1)
        return tokens

    @staticmethod
    def __append_token(tokens: List[Token], token: Token, end: int):
        if token:
            token.end = end
            token.normalized = token.text.lower()
            tokens.append(token)

    @staticmethod
    def __is_breaking_char(code_point: int):
        return (Tokenizer.__is_between(code_point, 0x0000, 0x002F) or
                Tokenizer.__is_between(code_point, 0x003A, 0x0040) or
                Tokenizer.__is_between(code_point, 0x005B, 0x0060) or
                Tokenizer.__is_between(code_point, 0x007B, 0x00BF) or
                Tokenizer.__is_between(code_point, 0x02B9, 0x036F) or
                Tokenizer.__is_between(code_point, 0x2000, 0x2BFF) or
                Tokenizer.__is_between(code_point, 0x2E00, 0x2E7F))

    @staticmethod
    def __is_between(value: int, start_from: int, to: int) -> bool:
        return start_from <= value <= to
