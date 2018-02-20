# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


import asyncio
from abc import *
from typing import *

from ..assertions import BotAssert


class Intent(object):
    def __init__(self, name: str=None, score: float=None, entities: List[object]=None):
        self.name = name
        self.score = score
        self.entities = entities


@abstractmethod
def intent_disabler(context): pass


@abstractmethod
def intent_recognizer(context): pass


@abstractmethod
def intent_result_mutators(context, intents: List[Intent]): pass


class IntentRecognizerMiddleware(object):
    def __init__(self):
        self._intent_disablers: List[intent_disabler] = []
        self._intent_recognizers: List[intent_recognizer] = []
        self._intent_result_mutators: List[intent_result_mutators] = []
        self._loop = asyncio.get_event_loop()

    async def receive_activity(self, context):
        BotAssert.context_not_none(context)

        intents: List[Intent] = await self.recognize(context)
        if len(intents) > 0:
            top_intent: Intent = IntentRecognizerMiddleware.find_top_intent(intents)
            if top_intent.score > 0.0:
                context.top_intent = top_intent

    async def recognize(self, context):
        BotAssert.context_not_none(context)
        is_enabled: bool = await self.is_recognizer_enabled(context)
        if is_enabled:
            all_recognized_intents: List[Intent] = await self.run_recognizer(context)
            await self.run_filters(context, all_recognized_intents)
            return all_recognized_intents
        else:
            return []

    async def run_recognizer(self, context):
        all_recognized_intents: List[Intent] = []
        for recognizer in self._intent_recognizers:
            intents: List[Intent] = await recognizer(context)
            if intents is not None and len(intents) > 0:
                all_recognized_intents.extend(intents)
        return all_recognized_intents

    async def is_recognizer_enabled(self, context):
        for user_code in self._intent_disablers:
            is_enabled: bool = await user_code(context)
            if is_enabled is False:
                return False
        return True

    async def run_filters(self, context, intents: List[Intent]):
        for filter in self._intent_result_mutators:
            await filter(context, intents)

    def on_enabled(self, pre_condition: intent_disabler):
        if pre_condition is None:
            raise TypeError()
        elif callable(pre_condition) is False:
            raise ValueError()
        self._intent_disablers.append(pre_condition)
        return self

    def on_recognize(self, recognizer: intent_recognizer):
        if recognizer is None:
            raise TypeError()
        elif callable(recognizer) is False:
            raise ValueError()
        self._intent_recognizers.append(recognizer)
        return self

    def on_filter(self, post_condition: intent_result_mutators):
        if post_condition is None:
            raise TypeError()
        elif callable(post_condition) is False:
            raise ValueError()
        self._intent_result_mutators.insert(0, post_condition)
        return self

    @staticmethod
    def find_top_intent(intents: List[Intent]):
        if intents is None:
            raise TypeError()
        if len(intents) <= 0:
            raise ValueError('No Intents found.')
        top_intent = intents[0]
        top_score = top_intent.score
        for intent in intents:
            if intent.score - top_score > 0:
                top_score = intent.score
                top_intent = intent
        return top_intent
