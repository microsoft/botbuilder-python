# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC
from .turn_context import TurnContext
from .recognizer_result import RecognizerResult


class Recognizer(ABC):
    @staticmethod
    async def recognize(turn_context: TurnContext) -> RecognizerResult:
        raise NotImplementedError()
