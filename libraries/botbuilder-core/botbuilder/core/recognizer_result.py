# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict, NamedTuple

from msrest.serialization import Model
from botbuilder.core import IntentScore


class TopIntent(NamedTuple):
    """The top scoring intent and its score."""

    intent: str
    score: float


class RecognizerResult(Model):
    """Contains recognition results generated by a recognizer."""

    _attribute_map = {
        "text": {"key": "text", "type": "str"},
        "altered_text": {"key": "alteredText", "type": "str"},
        "intents": {"key": "intents", "type": "{IntentScore}"},
        "entities": {"key": "entities", "type": "{object}"},
        "properties": {"key": "properties", "type": "{object}"},
    }

    def __init__(
        self,
        *,
        text: str = None,
        altered_text: str = None,
        intents: Dict[str, IntentScore] = None,
        entities: Dict[str, object] = None,
        properties: Dict[str, object] = None,
        **kwargs
    ):
        super(RecognizerResult, self).__init__(**kwargs)
        self.text = text
        self.altered_text = altered_text or kwargs.get("alteredText")
        self.intents = intents
        self.entities = entities
        self.properties = properties or {}

    def convert(self, result: object):
        self.text = result.text
        self.altered_text = result.altered_text
        self.intents = result.intents
        self.entities = result.entities
        self.properties = result.properties

    def get_top_scoring_intent(self) -> TopIntent:
        """Return the top scoring intent and its score.

        :return: Intent and score.
        :rtype: TopIntent
        """

        if self.intents is None:
            raise TypeError("result.intents can't be None")

        top_intent = TopIntent(intent="", score=0.0)
        for intent_name, intent_score in self.intents.items():
            score = intent_score.score
            if score > top_intent[1]:
                top_intent = TopIntent(intent_name, score)

        return top_intent
