# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from .bot_state import BotState
from .turn_context import TurnContext


class BotStateSet:
    def __init__(self, bot_states: List[BotState]):
        self.bot_states = list(bot_states)

    def add(self, bot_state: BotState) -> "BotStateSet":
        if bot_state is None:
            raise TypeError("Expected BotState")

        self.bot_states.append(bot_state)
        return self

    async def load_all(self, turn_context: TurnContext, force: bool = False):
        for bot_state in self.bot_states:
            await bot_state.load(turn_context, force)

    async def save_all_changes(self, turn_context: TurnContext, force: bool = False):
        for bot_state in self.bot_states:
            await bot_state.save_changes(turn_context, force)
