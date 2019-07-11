# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum


class DialogReason(Enum):
    # A dialog is being started through a call to `DialogContext.begin()`.
    BeginCalled = 1
    # A dialog is being continued through a call to `DialogContext.continue_dialog()`.
    ContinueCalled = 2
    # A dialog ended normally through a call to `DialogContext.end_dialog()`.
    EndCalled = 3
    # A dialog is ending because it's being replaced through a call to `DialogContext.replace_dialog()`.
    ReplaceCalled = 4
    # A dialog was cancelled as part of a call to `DialogContext.cancel_all_dialogs()`.
    CancelCalled = 5
    # A step was advanced through a call to `WaterfallStepContext.next()`.
    NextCalled = 6
