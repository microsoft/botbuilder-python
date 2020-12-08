# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs.memory import scope_path

from .memory_scope import MemoryScope


class DialogMemoryScope(MemoryScope):
    def __init__(self):
        # pylint: disable=import-outside-toplevel
        super().__init__(scope_path.DIALOG)

        # This import is to avoid circular dependency issues
        from botbuilder.dialogs import DialogContainer

        self._dialog_container_cls = DialogContainer

    def get_memory(self, dialog_context: "DialogContext") -> object:
        if not dialog_context:
            raise TypeError(f"Expecting: DialogContext, but received None")

        # if active dialog is a container dialog then "dialog" binds to it.
        if dialog_context.active_dialog:
            dialog = dialog_context.find_dialog_sync(dialog_context.active_dialog.id)
            if isinstance(dialog, self._dialog_container_cls):
                return dialog_context.active_dialog.state

        # Otherwise we always bind to parent, or if there is no parent the active dialog
        parent_state = (
            dialog_context.parent.active_dialog.state
            if dialog_context.parent and dialog_context.parent.active_dialog
            else None
        )
        dc_state = (
            dialog_context.active_dialog.state if dialog_context.active_dialog else None
        )
        return parent_state or dc_state

    def set_memory(self, dialog_context: "DialogContext", memory: object):
        if not dialog_context:
            raise TypeError(f"Expecting: DialogContext, but received None")

        if not memory:
            raise TypeError(f"Expecting: memory object, but received None")

        # If active dialog is a container dialog then "dialog" binds to it.
        # Otherwise the "dialog" will bind to the dialogs parent assuming it
        # is a container.
        parent = dialog_context
        if not self.is_container(parent) and self.is_container(parent.parent):
            parent = parent.parent

        # If there's no active dialog then throw an error.
        if not parent.active_dialog:
            raise Exception(
                "Cannot set DialogMemoryScope. There is no active dialog dialog or parent dialog in the context"
            )

        parent.active_dialog.state = memory

    def is_container(self, dialog_context: "DialogContext"):
        if dialog_context and dialog_context.active_dialog:
            dialog = dialog_context.find_dialog_sync(dialog_context.active_dialog.id)
            if isinstance(dialog, self._dialog_container_cls):
                return True

        return False
