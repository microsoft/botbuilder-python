# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import Iterable

from botbuilder.core import ComponentRegistration

from botbuilder.dialogs.memory import (
    ComponentMemoryScopesBase,
    ComponentPathResolversBase,
    PathResolverBase,
)
from botbuilder.dialogs.memory.scopes import MemoryScope


class DialogComponentRegistration(
    ComponentRegistration, ComponentMemoryScopesBase, ComponentPathResolversBase
):
    def get_memory_scopes(self) -> Iterable[MemoryScope]:
        pass

    def get_path_resolvers(self) -> Iterable[PathResolverBase]:
        pass
