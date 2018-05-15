# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from typing import List


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
    def __init__(self):
        self.e_tag = None
