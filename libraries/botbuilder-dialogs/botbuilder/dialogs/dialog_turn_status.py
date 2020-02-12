# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum


class DialogTurnStatus(Enum):
    """
    Indicates in which a dialog-related method is being called.

    :var Empty: Indicates that there is currently nothing on the dialog stack.
    :vartype Empty: int
    :var Waiting: Indicates that the dialog on top is waiting for a response from the user.
    :vartype Waiting: int
    :var Complete: Indicates that the dialog completed successfully, the result is available, and the stack is empty.
    :vartype Complete: int
    :var Cancelled: Indicates that the dialog was cancelled and the stack is empty.
    :vartype Cancelled: int
    """

    Empty = 1

    Waiting = 2

    Complete = 3

    Cancelled = 4
