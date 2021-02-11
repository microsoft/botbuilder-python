# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from .dialog_instance import DialogInstance


class DialogState:
    """
    Contains state information for the dialog stack.
    """

    def __init__(self, stack: List[DialogInstance] = None):
        """
        Initializes a new instance of the :class:`DialogState` class.

        :param stack: The state information to initialize the stack with.
        :type stack: :class:`typing.List`
        """
        if stack is None:
            self._dialog_stack = []
        else:
            self._dialog_stack = stack

    @property
    def dialog_stack(self):
        """
        Initializes a new instance of the :class:`DialogState` class.

        :return: The state information to initialize the stack with.
        :rtype: :class:`typing.List`
        """
        return self._dialog_stack

    def __str__(self):
        if not self._dialog_stack:
            return "dialog stack empty!"
        return " ".join(map(str, self._dialog_stack))
