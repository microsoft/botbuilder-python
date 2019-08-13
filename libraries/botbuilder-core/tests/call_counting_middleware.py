# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Awaitable, Callable
from botbuilder.core import Middleware, TurnContext


class CallCountingMiddleware(Middleware):
    def __init__(self):
        self.counter = 0

    def on_turn(  # pylint: disable=unused-argument
        self, context: TurnContext, logic: Callable[[TurnContext], Awaitable]
    ):
        self.counter += 1
        logic()
