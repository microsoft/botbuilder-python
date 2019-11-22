# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from .dialog_instance import DialogInstance


class DialogState:
    def __init__(self, stack: List[DialogInstance] = None):
        if stack is None:
            self.dialog_stack = []
        else:
            self.dialog_stack = stack

    def __str__(self):
        if not self.dialog_stack:
            return "dialog stack empty!"
        return " ".join(map(str, self.dialog_stack))
