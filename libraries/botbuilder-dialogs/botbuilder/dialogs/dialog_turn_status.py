# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum

class DialogTurnStatus(Enum):
    """Codes indicating the state of the dialog stack after a call to `DialogContext.continueDialog()`

    :var Empty: Indicates that there is currently nothing on the dialog stack.
    :vartype Empty: :class:`int`
    :var Waiting: Indicates that the dialog on top is waiting for a response from the user.
    :vartype Waiting: :class:`int`
    :var Complete: Indicates that the dialog completed successfully, the result is available, and the stack is empty.
    :vartype Complete: :class:`int`
    :var Cancelled: Indicates that the dialog was cancelled and the stack is empty.
    :vartype Cancelled: :class:`int`
    """
    
    Empty = 1

    Waiting = 2

    Complete = 3

    Cancelled = 4
