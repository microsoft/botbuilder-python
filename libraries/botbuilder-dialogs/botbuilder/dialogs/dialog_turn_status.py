# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum


class DialogTurnStatus(Enum):
    # Indicates that there is currently nothing on the dialog stack.
    Empty = 1

    # Indicates that the dialog on top is waiting for a response from the user.
    Waiting = 2

    # Indicates that the dialog completed successfully, the result is available, and the stack is empty.
    Complete = 3

    # Indicates that the dialog was cancelled and the stack is empty.
    Cancelled = 4
