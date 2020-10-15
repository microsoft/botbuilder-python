# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from copy import deepcopy

from botbuilder.dialogs import DialogContainer, DialogContext
from botbuilder.dialogs.memory import scope_path

from .memory_scope import MemoryScope


class DialogClassMemoryScope(MemoryScope):
    def __init__(self):
        super().__init__(scope_path.DIALOG_CLASS, include_in_snapshot=False)

    def get_memory(self, dialog_context: DialogContext) -> object:
        # if active dialog is a container dialog then "dialogclass" binds to it.
        if dialog_context.active_dialog:
            dialog = dialog_context.find_dialog(dialog_context.active_dialog.id)
            if isinstance(dialog, DialogContainer):
                return deepcopy(dialog)

        # Otherwise we always bind to parent, or if there is no parent the active dialog
        parent_id = (
            dialog_context.parent.active_dialog.id
            if dialog_context.parent and dialog_context.parent.active_dialog
            else None
        )
        active_id = (
            dialog_context.active_dialog.id if dialog_context.active_dialog else None
        )
        return deepcopy(dialog_context.find_dialog(parent_id or active_id))

    def set_memory(self, dialog_context: DialogContext, memory: object):
        raise Exception(
            f"{self.__class__.__name__}.set_memory not supported (read only)"
        )
