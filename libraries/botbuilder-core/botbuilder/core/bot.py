# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

from .turn_context import TurnContext


class Bot(ABC):
    """
    Represents a bot that can operate on incoming activities.
    """

    @abstractmethod
    async def on_turn(self, context: TurnContext):
        """
        When implemented in a bot, handles an incoming activity.
        :param context: The context object for this turn.
        :return:
        """
        raise NotImplementedError()
