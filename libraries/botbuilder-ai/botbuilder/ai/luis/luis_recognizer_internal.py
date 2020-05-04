# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from botbuilder.core import TurnContext
from .luis_application import LuisApplication


class LuisRecognizerInternal(ABC):
    def __init__(self, luis_application: LuisApplication):
        if luis_application is None:
            raise TypeError(luis_application.__class__.__name__)

        self.luis_application = luis_application

    @abstractmethod
    async def recognizer_internal(self, turn_context: TurnContext):
        raise NotImplementedError()
