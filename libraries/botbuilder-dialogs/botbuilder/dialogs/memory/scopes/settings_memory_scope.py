# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs.memory import scope_path

from .memory_scope import MemoryScope


class SettingsMemoryScope(MemoryScope):
    def __init__(self):
        super().__init__(scope_path.SETTINGS)
        self._empty_settings = {}
        self.include_in_snapshot = False

    def get_memory(self, dialog_context: "DialogContext") -> object:
        if not dialog_context:
            raise TypeError(f"Expecting: DialogContext, but received None")

        settings: dict = dialog_context.context.turn_state.get(
            scope_path.SETTINGS, None
        )

        if not settings:
            settings = self._empty_settings

        return settings

    def set_memory(self, dialog_context: "DialogContext", memory: object):
        raise Exception(
            f"{self.__class__.__name__}.set_memory not supported (read only)"
        )
