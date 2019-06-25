# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Union

from .token import Token

class Tokenizer:
    """ Provides a default tokenizer implementation. """

    @staticmethod
    def default_tokenizer(text: str, locale: str = None) -> [Token]:
        tokens: [Token] = []
        token: Union[Token, None] = None

        # Parse text
        length: int = len(text) if text else 0
        i: int = 0

        while i < length:
            # Get botht he UNICODE value of the current character and the complete character itself
            # which can potentially be multiple segments
            code_point = ord(text[i])
            char = chr(code_point)

            # Process current character
            # WRITE IsBreakingChar(code_point)
    
    # def _is