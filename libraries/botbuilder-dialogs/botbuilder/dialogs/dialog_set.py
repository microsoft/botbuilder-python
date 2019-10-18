# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import inspect
from typing import Dict

from botbuilder.core import TurnContext, BotAssert, StatePropertyAccessor
from .dialog import Dialog
from .dialog_state import DialogState
from .dialog_context import DialogContext


class DialogSet:
    def __init__(self, dialog_state: StatePropertyAccessor = None):
        if dialog_state is None:
            frame = inspect.currentframe().f_back
            try:
                # try to access the caller's "self"
                try:
                    self_obj = frame.f_locals["self"]
                except KeyError:
                    raise TypeError("DialogSet(): dialog_state cannot be None.")
                # Only ComponentDialog can initialize with None dialog_state
                # pylint: disable=import-outside-toplevel
                from .component_dialog import ComponentDialog

                if not isinstance(self_obj, ComponentDialog):
                    raise TypeError("DialogSet(): dialog_state cannot be None.")
            finally:
                # make sure to clean up the frame at the end to avoid ref cycles
                del frame

        self._dialog_state = dialog_state
        # self.__telemetry_client = NullBotTelemetryClient.Instance;

        self._dialogs: Dict[str, object] = {}

    def add(self, dialog: Dialog):
        """
        Adds a new dialog to the set and returns the added dialog.
        :param dialog: The dialog to add.
        """
        if dialog is None or not isinstance(dialog, Dialog):
            raise TypeError(
                "DialogSet.add(): dialog cannot be None and must be a Dialog or derived class."
            )

        if dialog.id in self._dialogs:
            raise TypeError(
                "DialogSet.add(): A dialog with an id of '%s' already added."
                % dialog.id
            )

        # dialog.telemetry_client = this._telemetry_client;
        self._dialogs[dialog.id] = dialog

        return self

    async def create_context(self, turn_context: TurnContext) -> DialogContext:
        # pylint: disable=unnecessary-lambda
        BotAssert.context_not_none(turn_context)

        if not self._dialog_state:
            raise RuntimeError(
                "DialogSet.CreateContextAsync(): DialogSet created with a null IStatePropertyAccessor."
            )

        state = await self._dialog_state.get(turn_context, lambda: DialogState())

        return DialogContext(self, turn_context, state)

    async def find(self, dialog_id: str) -> Dialog:
        """
        Finds a dialog that was previously added to the set using add(dialog)
        :param dialog_id: ID of the dialog/prompt to look up.
        :return: The dialog if found, otherwise null.
        """
        if not dialog_id:
            raise TypeError("DialogContext.find(): dialog_id cannot be None.")

        if dialog_id in self._dialogs:
            return self._dialogs[dialog_id]

        return None

    def __str__(self):
        if self._dialogs:
            return "dialog set empty!"
        return " ".join(map(str, self._dialogs.keys()))
