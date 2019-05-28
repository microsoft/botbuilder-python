# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Callable
from botbuilder.core import Middleware, TurnContext

class CallCountingMiddleware(Middleware):

    def __init__(self):
        self.counter = 0

    def on_process_request(self, context: TurnContext, next: Callable):
        self.counter += 1
        next()