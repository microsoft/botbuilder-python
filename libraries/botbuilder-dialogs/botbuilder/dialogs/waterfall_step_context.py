# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict

from .dialog_context import DialogContext
from .dialog_reason import DialogReason
from .dialog_turn_result import DialogTurnResult
from .dialog_state import DialogState


class WaterfallStepContext(DialogContext):
    def __init__(
        self,
        parent,
        dc: DialogContext,
        options: object,
        values: Dict[str, object],
        index: int,
        reason: DialogReason,
        result: object = None,
    ):
        super(WaterfallStepContext, self).__init__(
            dc.dialogs, dc.context, DialogState(dc.stack)
        )
        self._wf_parent = parent
        self._next_called = False
        self._index = index
        self._options = options
        self._reason = reason
        self._result = result
        self._values = values
        self.parent = dc.parent

    @property
    def index(self) -> int:
        return self._index

    @property
    def options(self) -> object:
        return self._options

    @property
    def reason(self) -> DialogReason:
        return self._reason

    @property
    def result(self) -> object:
        return self._result

    @property
    def values(self) -> Dict[str, object]:
        return self._values

    async def next(self, result: object) -> DialogTurnResult:
        if self._next_called is True:
            raise Exception(
                "WaterfallStepContext.next(): method already called for dialog and step '%s'[%s]."
                % (self._wf_parent.id, self._index)
            )

        # Trigger next step
        self._next_called = True
        return await self._wf_parent.resume_dialog(
            self, DialogReason.NextCalled, result
        )
