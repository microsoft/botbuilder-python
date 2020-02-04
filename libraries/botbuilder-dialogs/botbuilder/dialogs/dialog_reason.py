# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum

class DialogReason(Enum):
    """
    Indicates in which a dialog-related method is being called.
    """

    """
    A dialog is being started through a call to :meth:`DialogContext.begin()`.
    """
    BeginCalled = 1

    """
    A dialog is being continued through a call to
    :meth:`DialogContext.continue_dialog()`.
    """
    ContinueCalled = 2

    """
    A dialog ended normally through a call to :meth:`DialogContext.end_dialog().
    """
    EndCalled = 3

    """
    A dialog is ending because it's being replaced through a call to
    :meth:`DialogContext.replace_dialog()`.
    """
    ReplaceCalled = 4

    """
    A dialog was cancelled as part of a call to
    :meth:`DialogContext.cancel_all_dialogs()`.
    """
    CancelCalled = 5

    """
    A preceding step was skipped through a call to
    :meth:`WaterfallStepContext.next()`.
    """
    NextCalled = 6
