# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict, List
from botbuilder.core import BotState
from .dialog_instance import DialogInstance


class DialogState:
    def __init__(self, stack: List[DialogInstance] = None):
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


def serializer(dialog_state: DialogState) -> Dict[str, List]:
    return dict(stack=dialog_state.dialog_stack)


def deserializer(data: Dict[str, List]) -> DialogState:
    return DialogState(data["stack"])


BotState.register_serialization_functions(DialogState, serializer, deserializer)
