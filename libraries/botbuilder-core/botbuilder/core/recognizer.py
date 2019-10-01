# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from .turn_context import TurnContext
from .recognizer_result import RecognizerResult


class Recognizer(ABC):
    @abstractmethod
    async def recognize(self, turn_context: TurnContext) -> RecognizerResult:
        raise NotImplementedError()
