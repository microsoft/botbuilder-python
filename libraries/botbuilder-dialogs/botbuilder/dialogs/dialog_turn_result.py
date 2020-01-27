# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .dialog_turn_status import DialogTurnStatus

class DialogTurnResult:
    """ 
    Result returned to the caller of one of the various stack manipulation methods.

    Use :meth:`DialogContext.end_dialogAsync()` to end a :class:`Dialog` and
    return a result to the calling context.
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
       
    @property
    def result(self):
        """
        Final result returned by a dialog that just completed.
        
       .. note::
           This will only be populated in certain cases:
           * The bot calls :meth:`DialogContext.begin_dialog()` to start a new dialog and the dialog ends immediately.
           * The bot calls :meth:`DialogContext.continue_dialog()` and a dialog that was active ends.

    :return self._result: Final result returned by a dialog that just completed.
    :rtype self._result: object
    """
        return self._result
