# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum


class DialogTurnStatus(Enum):
    """
    Codes indicating the state of the dialog stack after a call to `DialogContext.continueDialog()`
    """

    Empty = 1
    """
    Indicates that there is currently nothing on the dialog stack.
    """

    Waiting = 2
    """
    Indicates that the dialog on top is waiting for a response from the user.
    """

    Complete = 3
    """
    Indicates that the dialog completed successfully, the result is available, and the stack is empty.
    """

    Cancelled = 4
    """
    Indicates that the dialog was cancelled and the stack is empty.
    """
