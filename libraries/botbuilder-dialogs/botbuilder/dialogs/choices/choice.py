# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.schema import CardAction


class Choice:
    def __init__(
        self, value: str = None, action: CardAction = None, synonyms: List[str] = None
    ):
        self.value: str = value
        self.action: CardAction = action
        self.synonyms: List[str] = synonyms
