# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.schema import Activity

from .dialog_turn_result import DialogTurnResult
from .persisted_state import PersistedState


class DialogManagerResult:
    def __init__(self):
        self.turn_result: DialogTurnResult = None
        self.activities: List[Activity] = None
        self.persisted_state: PersistedState = None
