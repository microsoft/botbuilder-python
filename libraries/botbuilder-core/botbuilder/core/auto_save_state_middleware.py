# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Awaitable, Callable, List, Union

from .bot_state import BotState
from .bot_state_set import BotStateSet
from .middleware_set import Middleware
from .turn_context import TurnContext


class AutoSaveStateMiddleware(Middleware):
    def __init__(self, bot_states: Union[List[BotState], BotStateSet] = None):
        if bot_states is None:
            bot_states = []
        if isinstance(bot_states, BotStateSet):
            self.bot_state_set: BotStateSet = bot_states
        else:
            self.bot_state_set: BotStateSet = BotStateSet(bot_states)

    def add(self, bot_state: BotState) -> "AutoSaveStateMiddleware":
        if bot_state is None:
            raise TypeError("Expected BotState")

        self.bot_state_set.add(bot_state)
        return self

    async def on_turn(
        self, context: TurnContext, logic: Callable[[TurnContext], Awaitable]
    ):
        await logic()
        await self.bot_state_set.save_all_changes(context, False)
