# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

from .turn_context import TurnContext


class StatePropertyAccessor(ABC):
    @abstractmethod
    async def get(
        self, turn_context: TurnContext, default_value_or_factory=None
    ) -> object:
        """
        Get the property value from the source
        :param turn_context: Turn Context.
        :param default_value_or_factory: Function which defines the property
        value to be returned if no value has been set.

        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, turn_context: TurnContext) -> None:
        """
        Saves store items to storage.
        :param turn_context: Turn Context.
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def set(self, turn_context: TurnContext, value) -> None:
        """
        Set the property value on the source.
        :param turn_context: Turn Context.
        :param value:
        :return:
        """
        raise NotImplementedError()
