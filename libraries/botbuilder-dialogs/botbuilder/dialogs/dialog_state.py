# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from .dialog_instance import DialogInstance
from typing import List

class DialogState():

    def __init__(self, stack: List[DialogInstance] = None):
        if stack == None:
            self._dialog_stack = []
        else:
            self._dialog_stack = stack
        
    @property
    def dialog_stack(self):
        return self._dialog_stack

    def __str__(self):
        if len(self._dialog_stack) <= 0:
            return "dialog stack empty!"
        return ' '.join(map(str, self._dialog_stack))

