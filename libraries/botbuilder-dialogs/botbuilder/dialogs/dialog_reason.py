# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum

"""
NOTE: Multiple formats added, will remove whatever formatting isn't needed
"""

class DialogReason(Enum):
    """ Indicates in which a dialog-related method is being called.
    :var BeginCalled: A dialog is being started through a call to `DialogContext.begin()`.
    :vartype BeginCalled: int
    :var ContinuCalled: A dialog is being continued through a call to `DialogContext.continue_dialog()`.
    :vartype ContinueCalled: int
    :var EndCalled: A dialog ended normally through a call to `DialogContext.end_dialog()
    :vartype EndCalled: int
    :var ReplaceCalled: A dialog is ending because it's being replaced through a call to `DialogContext.replace_dialog()`.
    :vartype ReplacedCalled: int
    :var CancelCalled: A dialog was cancelled as part of a call to `DialogContext.cancel_all_dialogs()`.
    :vartype CancelCalled: int
    :var NextCalled: A preceding step was skipped through a call to `WaterfallStepContext.next()`.
    :vartype NextCalled: int
    """
    
    """
    A dialog is being started through a call to `DialogContext.begin()`.
    """
    BeginCalled = 1
    """
    A dialog is being continued through a call to `DialogContext.continue_dialog()`.
    """
    ContinueCalled = 2
    """
    A dialog ended normally through a call to `DialogContext.end_dialog()
    """
    EndCalled = 3
    """
    A dialog is ending because it's being replaced through a call to `DialogContext.replace_dialog()`.
    """
    ReplaceCalled = 4
    """
    A dialog was cancelled as part of a call to `DialogContext.cancel_all_dialogs()`.
    """
    CancelCalled = 5
    """
    A preceding step was skipped through a call to `WaterfallStepContext.next()`.
    """
    NextCalled = 6
