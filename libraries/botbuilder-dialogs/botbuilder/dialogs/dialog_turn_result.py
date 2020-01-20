# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .dialog_turn_status import DialogTurnStatus

class DialogTurnResult:
    """ 
    Result returned to the caller of one of the various stack manipulation methods.
    """
    def __init__(self, status: DialogTurnStatus, result: object = None):
    """
    :param status: The current status of the stack.
    :type status: :class:`DialogTurnStatus`
    :param result: The result returned by a dialog that was just ended.
    :type result: object
    """
        self._status = status
        self._result = result
        
    @property
    def status(self):
    """
    Gets or sets the current status of the stack.

    :return self._status:
    :rtype self._status: :class:`DialogTurnStatus`

    """
        return self._status
        
    """
    Final result returned by a dialog that just completed.
        ..remarks:
             This will only be populated in certain cases:
             - The bot calls `DialogContext.begin_dialog()` to start a new dialog and the dialog ends immediately.
             - The bot calls `DialogContext.continue_dialog()` and a dialog that was active ends.

    :return self._result: 
    :rtype self._result: object
    """
    @property
    def result(self):
        return self._result
