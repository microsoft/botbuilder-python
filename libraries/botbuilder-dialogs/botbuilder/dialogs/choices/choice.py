# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from msrest.serialization import Model
from botbuilder.schema import CardAction


class Choice(Model):
    _attribute_map = {
        "value": {"key": "value", "type": "str"},
        "action": {"key": "action", "type": "CardAction"},
        "synonyms": {"key": "synonyms", "type": "[str]"},
    }

    def __init__(
        self, value: str = None, action: CardAction = None, synonyms: List[str] = None, **kwargs
    ):
        super().__init__(**kwargs)
        self.value: str = value
        self.action: CardAction = action
        self.synonyms: List[str] = synonyms
