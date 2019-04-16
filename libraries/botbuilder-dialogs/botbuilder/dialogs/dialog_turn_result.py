# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .dialog_turn_status import DialogTurnStatus

class DialogTurnResult():

    def __init__(self, status: DialogTurnStatus, result:object = None):
        self.__status = status
        self.__result = result;
        
    @property
    def status(self):
        return __status;
    
    @property
    def result(self):
        return __result;
