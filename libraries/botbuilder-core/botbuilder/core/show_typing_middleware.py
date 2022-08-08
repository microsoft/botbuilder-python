# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import asyncio
from typing import Awaitable, Callable

from botbuilder.schema import Activity, ActivityTypes
from botframework.connector.auth import ClaimsIdentity, SkillValidation

from .bot_adapter import BotAdapter
from .middleware_set import Middleware
from .turn_context import TurnContext


class Timer:
    clear_timer = False

    def set_timeout(self, func, span):
        async def some_fn():  # pylint: disable=function-redefined
            await asyncio.sleep(span)
            if not self.clear_timer:
                await func()

        asyncio.ensure_future(some_fn())

    def set_clear_timer(self):
        self.clear_timer = True


class ShowTypingMiddleware(Middleware):
    """
    When added, this middleware will send typing activities back to the user when a Message activity
    is received to let them know that the bot has received the message and is working on the response.
    You can specify a delay before the first typing activity is sent and then a frequency, which
    determines how often another typing activity is sent. Typing activities will continue to be sent
    until your bot sends another message back to the user.
    """

    def __init__(self, delay: float = 0.5, period: float = 2.0):
        """
        Initializes the middleware.

        :param delay: Delay in seconds for the first typing indicator to be sent.
        :param period: Delay in seconds for subsequent typing indicators.
        """

        if delay < 0:
            raise ValueError("Delay must be greater than or equal to zero")

        if period <= 0:
            raise ValueError("Repeat period must be greater than zero")

        self._delay = delay
        self._period = period

    async def on_turn(
        self, context: TurnContext, logic: Callable[[TurnContext], Awaitable]
    ):
        timer = Timer()

        def start_interval(context: TurnContext, delay, period):
            async def aux():
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

                asyncio.ensure_future(
                    context.adapter.send_activities(context, [typing_activity])
                )

                # restart the timer, with the 'period' value for the delay
                timer.set_timeout(aux, period)

            # first time through we use the 'delay' value for the timer.
            timer.set_timeout(aux, delay)

        def stop_interval():
            timer.set_clear_timer()

        # Start a timer to periodically send the typing activity
        # (bots running as skills should not send typing activity)
        if (
            context.activity.type == ActivityTypes.message
            and not ShowTypingMiddleware._is_skill_bot(context)
        ):
            start_interval(context, self._delay, self._period)

        # call the bot logic
        result = await logic()

        stop_interval()

        return result

    @staticmethod
    def _is_skill_bot(context: TurnContext) -> bool:
        claims_identity = context.turn_state.get(BotAdapter.BOT_IDENTITY_KEY)
        return isinstance(
            claims_identity, ClaimsIdentity
        ) and SkillValidation.is_skill_claim(claims_identity.claims)
