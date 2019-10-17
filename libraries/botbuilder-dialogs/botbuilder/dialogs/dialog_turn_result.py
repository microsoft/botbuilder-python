# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .dialog_turn_status import DialogTurnStatus


class DialogTurnResult:
    def __init__(self, status: DialogTurnStatus, result: object = None):
        self._status = status
        self._result = result

    @property
    def status(self):
        return self._status

    @property
    def result(self):
        return self._result
