# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum


class DialogReason(Enum):
    """
    Indicates in which a dialog-related method is being called.

    :var BeginCalled: A dialog is being started through a call to :meth:`DialogContext.begin()`.
    :vartype BeginCalled: int
    :var ContinueCalled: A dialog is being continued through a call to :meth:`DialogContext.continue_dialog()`.
    :vartype ContinueCalled: int
    :var EndCalled: A dialog ended normally through a call to :meth:`DialogContext.end_dialog()
    :vartype EndCalled: int
    :var ReplaceCalled: A dialog is ending and replaced through a call to :meth:``DialogContext.replace_dialog()`.
    :vartype ReplacedCalled: int
    :var CancelCalled: A dialog was cancelled as part of a call to :meth:`DialogContext.cancel_all_dialogs()`.
    :vartype CancelCalled: int
    :var NextCalled: A preceding step was skipped through a call to :meth:`WaterfallStepContext.next()`.
    :vartype NextCalled: int
    """

    BeginCalled = 1

    ContinueCalled = 2

    EndCalled = 3

    ReplaceCalled = 4

    CancelCalled = 5

    NextCalled = 6
