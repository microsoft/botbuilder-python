# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import Callable, Awaitable

from botbuilder.core import Middleware, TurnContext


class RegisterClassMiddleware(Middleware):
    """
    Middleware for adding an object to or registering a service with the current turn context.
    """

    def __init__(self, service, key: str = None):
        self.service = service
        self._key = key

    async def on_turn(
        self, context: TurnContext, logic: Callable[[TurnContext], Awaitable]
    ):
        # C# has TurnStateCollection with has overrides for adding items
        # to TurnState.  Python does not.  In C#'s case, there is an 'Add'
        # to handle adding object, and that uses the fully qualified class name.
        key = self._key or self.fullname(self.service)
        context.turn_state[key] = self.service
        await logic()

    @staticmethod
    def fullname(obj):
        module = obj.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return obj.__class__.__name__  # Avoid reporting __builtin__
        return module + "." + obj.__class__.__name__
