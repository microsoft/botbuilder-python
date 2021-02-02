from typing import List

from botbuilder.dialogs.memory.scopes import MemoryScope
from .path_resolver_base import PathResolverBase


class DialogStateManagerConfiguration:
    def __init__(self):
        self.path_resolvers: List[PathResolverBase] = list()
        self.memory_scopes: List[MemoryScope] = list()
