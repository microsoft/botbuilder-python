# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from collections import namedtuple

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
            dialog = dialog_context.find_dialog_sync(dialog_context.active_dialog.id)
            if dialog:
                return ClassMemoryScope._bind_to_dialog_context(dialog, dialog_context)

        return None

    def set_memory(self, dialog_context: "DialogContext", memory: object):
        raise Exception(
            f"{self.__class__.__name__}.set_memory not supported (read only)"
        )

    @staticmethod
    def _bind_to_dialog_context(obj, dialog_context: "DialogContext") -> object:
        clone = {}
        for prop in dir(obj):
            # don't process double underscore attributes
            if prop[:1] != "_":
                prop_value = getattr(obj, prop)
                if not callable(prop_value):
                    # the only objects
                    if hasattr(prop_value, "try_get_value"):
                        clone[prop] = prop_value.try_get_value(dialog_context.state)
                    elif hasattr(prop_value, "__dict__") and not isinstance(
                        prop_value, type(prop_value)
                    ):
                        clone[prop] = ClassMemoryScope._bind_to_dialog_context(
                            prop_value, dialog_context
                        )
                    else:
                        clone[prop] = prop_value
        if clone:
            ReadOnlyObject = namedtuple(  # pylint: disable=invalid-name
                "ReadOnlyObject", clone
            )
            return ReadOnlyObject(**clone)

        return None
