# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


from abc import ABC, abstractmethod
from typing import Iterable

from botbuilder.dialogs.memory.scopes import MemoryScope


class ComponentMemoryScopesBase(ABC):
    @abstractmethod
    def get_memory_scopes(self) -> Iterable[MemoryScope]:
        raise NotImplementedError()
