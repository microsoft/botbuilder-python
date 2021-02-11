# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Type

from botbuilder.core import BotState

from .memory_scope import MemoryScope


class BotStateMemoryScope(MemoryScope):
    def __init__(self, bot_state_type: Type[BotState], name: str):
        super().__init__(name, include_in_snapshot=True)
        self.bot_state_type = bot_state_type

    def get_memory(self, dialog_context: "DialogContext") -> object:
        if not dialog_context:
            raise TypeError(f"Expecting: DialogContext, but received None")

        bot_state: BotState = self._get_bot_state(dialog_context)
        cached_state = (
            bot_state.get_cached_state(dialog_context.context) if bot_state else None
        )

        return cached_state.state if cached_state else None

    def set_memory(self, dialog_context: "DialogContext", memory: object):
        raise RuntimeError("You cannot replace the root BotState object")

    async def load(self, dialog_context: "DialogContext", force: bool = False):
        bot_state: BotState = self._get_bot_state(dialog_context)

        if bot_state:
            await bot_state.load(dialog_context.context, force)

    async def save_changes(self, dialog_context: "DialogContext", force: bool = False):
        bot_state: BotState = self._get_bot_state(dialog_context)

        if bot_state:
            await bot_state.save_changes(dialog_context.context, force)

    def _get_bot_state(self, dialog_context: "DialogContext") -> BotState:
        return dialog_context.context.turn_state.get(self.bot_state_type.__name__, None)
