# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from copy import copy
from abc import ABC, abstractmethod
from typing import Callable, List

from .turn_context import TurnContext


class Storage(ABC):
    @abstractmethod
    async def read(self, keys: List[str]):
        """
        Loads store items from storage.
        :param keys:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def write(self, changes):
        """
        Saves store items to storage.
        :param changes:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, keys: List[str]):
        """
        Removes store items from storage.
        :param keys:
        :return:
        """
        raise NotImplementedError()


class StoreItem(ABC):
    """
    Object which is stored in Storage with an optional eTag.
    """
    def __init__(self, **kwargs):
        # If e_tag is passed in as a kwarg use that value, otherwise assign the wildcard value to the new e_tag
        self.e_tag = kwargs.get('e_tag', '*')
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        non_magic_attributes = [attr for attr in dir(self) if not attr.startswith('_')]
        output = '{' + ','.join(
            [f" '{attr}': '{getattr(self, attr)}'" for attr in non_magic_attributes]) + ' }'
        return output


StorageKeyFactory = Callable[[TurnContext], str]


def calculate_change_hash(item: StoreItem) -> str:
    """
    Utility function to calculate a change hash for a `StoreItem`.
    :param item:
    :return:
    """
    cpy = copy(item)
    if cpy.e_tag is not None:
        del cpy.e_tag
    return str(cpy)
