# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import Iterable

from botbuilder.core import ComponentRegistration

from botbuilder.dialogs.memory import (
    ComponentMemoryScopesBase,
    ComponentPathResolversBase,
    PathResolverBase,
)
from botbuilder.dialogs.memory.scopes import (
    TurnMemoryScope,
    SettingsMemoryScope,
    DialogMemoryScope,
    DialogContextMemoryScope,
    DialogClassMemoryScope,
    ClassMemoryScope,
    MemoryScope,
    ThisMemoryScope,
    ConversationMemoryScope,
    UserMemoryScope,
)

from botbuilder.dialogs.memory.path_resolvers import (
    AtAtPathResolver,
    AtPathResolver,
    DollarPathResolver,
    HashPathResolver,
    PercentPathResolver,
)


class DialogsComponentRegistration(
    ComponentRegistration, ComponentMemoryScopesBase, ComponentPathResolversBase
):
    def get_memory_scopes(self) -> Iterable[MemoryScope]:
        yield TurnMemoryScope()
        yield SettingsMemoryScope()
        yield DialogMemoryScope()
        yield DialogContextMemoryScope()
        yield DialogClassMemoryScope()
        yield ClassMemoryScope()
        yield ThisMemoryScope()
        yield ConversationMemoryScope()
        yield UserMemoryScope()

    def get_path_resolvers(self) -> Iterable[PathResolverBase]:
        yield AtAtPathResolver()
        yield AtPathResolver()
        yield DollarPathResolver()
        yield HashPathResolver()
        yield PercentPathResolver()
