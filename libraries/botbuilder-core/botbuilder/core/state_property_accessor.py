# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from copy import copy
from abc import ABC, abstractmethod
from typing import Callable, List

from .turn_context import TurnContext


class StatePropertyAccessor(ABC):
    @abstractmethod
    async def get(self, turnContext: TurnContext, default_value_factory = None):
        """
        Get the property value from the source
        :param turn_context: Turn Context.
        :param default_value_factory: Function which defines the property value to be returned if no value has been set.

        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, turnContext: TurnContext):
        """
        Saves store items to storage.
        :param turn_context: Turn Context.
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def set(self, turnContext: TurnContext, value):
        """
        Set the property value on the source.
        :param turn_context: Turn Context.
        :return:
        """
        raise NotImplementedError()

