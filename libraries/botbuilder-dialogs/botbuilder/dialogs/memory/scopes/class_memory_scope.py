# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from copy import deepcopy

from botbuilder.dialogs.memory import scope_path

from .memory_scope import MemoryScope


class ClassMemoryScope(MemoryScope):
    def __init__(self):
        super().__init__(scope_path.SETTINGS, include_in_snapshot=False)

    def get_memory(self, dialog_context: "DialogContext") -> object:
        if not dialog_context:
            raise TypeError(f"Expecting: DialogContext, but received None")

        # if active dialog is a container dialog then "dialogclass" binds to it.
        if dialog_context.active_dialog:
            dialog = dialog_context.find_dialog(dialog_context.active_dialog.id)
            if dialog:
                return deepcopy(dialog)

        return None

    def set_memory(self, dialog_context: "DialogContext", memory: object):
        raise Exception(
            f"{self.__class__.__name__}.set_memory not supported (read only)"
        )
