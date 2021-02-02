# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs.memory import scope_path

from .memory_scope import MemoryScope


class ThisMemoryScope(MemoryScope):
    def __init__(self):
        super().__init__(scope_path.THIS)

    def get_memory(self, dialog_context: "DialogContext") -> object:
        if not dialog_context:
            raise TypeError(f"Expecting: DialogContext, but received None")

        return (
            dialog_context.active_dialog.state if dialog_context.active_dialog else None
        )

    def set_memory(self, dialog_context: "DialogContext", memory: object):
        if not dialog_context:
            raise TypeError(f"Expecting: DialogContext, but received None")

        if not memory:
            raise TypeError(f"Expecting: object, but received None")

        dialog_context.active_dialog.state = memory
