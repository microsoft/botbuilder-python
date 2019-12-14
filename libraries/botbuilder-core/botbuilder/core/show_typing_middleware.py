# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import time
from functools import wraps
from typing import Awaitable, Callable

from botbuilder.schema import Activity, ActivityTypes

from .middleware_set import Middleware
from .turn_context import TurnContext


def delay(span=0.0):
    def wrap(func):
        @wraps(func)
        async def delayed():
            time.sleep(span)
            await func()

        return delayed

    return wrap


class Timer:
    clear_timer = False

    async def set_timeout(self, func, time):
        is_invocation_cancelled = False

        @delay(time)
        async def some_fn():  # pylint: disable=function-redefined
            if not self.clear_timer:
                await func()

        await some_fn()
        return is_invocation_cancelled

    def set_clear_timer(self):
        self.clear_timer = True


class ShowTypingMiddleware(Middleware):
    def __init__(self, delay: float = 0.5, period: float = 2.0):
        if delay < 0:
            raise ValueError("Delay must be greater than or equal to zero")

        if period <= 0:
            raise ValueError("Repeat period must be greater than zero")

        self._delay = delay
        self._period = period

    async def on_turn(
        self, context: TurnContext, logic: Callable[[TurnContext], Awaitable]
    ):
        finished = False
        timer = Timer()

        async def start_interval(context: TurnContext, delay: int, period: int):
            async def aux():
                if not finished:
                    typing_activity = Activity(
                        type=ActivityTypes.typing,
                        relates_to=context.activity.relates_to,
                    )

                    conversation_reference = TurnContext.get_conversation_reference(
                        context.activity
                    )

                    typing_activity = TurnContext.apply_conversation_reference(
                        typing_activity, conversation_reference
                    )

                    await context.adapter.send_activities(context, [typing_activity])

                    start_interval(context, period, period)

            await timer.set_timeout(aux, delay)

        def stop_interval():
            nonlocal finished
            finished = True
            timer.set_clear_timer()

        if context.activity.type == ActivityTypes.message:
            finished = False
            await start_interval(context, self._delay, self._period)

        result = await logic()
        stop_interval()

        return result
