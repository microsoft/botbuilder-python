# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


from abc import ABC, abstractmethod
from typing import Iterable

from .path_resolver_base import PathResolverBase


class ComponentPathResolversBase(ABC):
    @abstractmethod
    def get_path_resolvers(self) -> Iterable[PathResolverBase]:
        raise NotImplementedError()
