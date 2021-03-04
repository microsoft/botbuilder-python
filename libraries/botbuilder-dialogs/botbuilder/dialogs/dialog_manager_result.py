# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.schema import Activity

from .dialog_turn_result import DialogTurnResult
from .persisted_state import PersistedState


class DialogManagerResult:
    def __init__(
        self,
        turn_result: DialogTurnResult = None,
        activities: List[Activity] = None,
        persisted_state: PersistedState = None,
    ):
        self.turn_result = turn_result
        self.activities = activities
        self.persisted_state = persisted_state
