# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from msrest.serialization import Model
from botbuilder.core import BotState
from .dialog_instance import DialogInstance


class DialogState(Model):
    _attribute_map = {
        "_dialog_stack": {"key": "stack", "type": "[DialogInstance]"}
    }

    def __init__(self, stack: List[DialogInstance] = None, **kwargs):
        super(DialogState, self).__init__(**kwargs)
        if stack is None:
            self._dialog_stack = []
        else:
            self._dialog_stack = stack

    @property
    def dialog_stack(self):
        return self._dialog_stack

    def __str__(self):
        if not self._dialog_stack:
            return "dialog stack empty!"
        return " ".join(map(str, self._dialog_stack))


BotState.register_msrest_deserializer(DialogState, dependencies=[DialogInstance])
