# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Awaitable, Callable
from botbuilder.core import Middleware, TurnContext


class CallCountingMiddleware(Middleware):
    def __init__(self):
        self.counter = 0

<<<<<<< HEAD
    def on_process_request(
=======
    def on_process_request(  # pylint: disable=unused-argument
>>>>>>> 6cc2e000be86f67297d21128216a763ba0f4ad78
        self, context: TurnContext, logic: Callable[[TurnContext], Awaitable]
    ):
        self.counter += 1
        logic()
