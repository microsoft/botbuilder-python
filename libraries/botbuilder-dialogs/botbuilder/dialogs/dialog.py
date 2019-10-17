# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from abc import ABC, abstractmethod

from botbuilder.core import TurnContext, NullTelemetryClient, BotTelemetryClient
from .dialog_reason import DialogReason
from .dialog_turn_status import DialogTurnStatus
from .dialog_turn_result import DialogTurnResult
from .dialog_instance import DialogInstance


class Dialog(ABC):
    end_of_turn = DialogTurnResult(DialogTurnStatus.Waiting)

    def __init__(self, dialog_id: str):
        if dialog_id is None or not dialog_id.strip():
            raise TypeError("Dialog(): dialogId cannot be None.")

        self._telemetry_client = NullTelemetryClient()
        self._id = dialog_id

    @property
    def id(self) -> str:  # pylint: disable=invalid-name
        return self._id

    @property
    def telemetry_client(self) -> BotTelemetryClient:
        """
        Gets the telemetry client for logging events.
        """
        return self._telemetry_client

    @telemetry_client.setter
    def telemetry_client(self, value: BotTelemetryClient) -> None:
        """
        Sets the telemetry client for logging events.
        """
        if value is None:
            self._telemetry_client = NullTelemetryClient()
        else:
            self._telemetry_client = value

    @abstractmethod
    async def begin_dialog(
        self, dialog_context: "DialogContext", options: object = None
    ):
        """
        Method called when a new dialog has been pushed onto the stack and is being activated.
        :param dialog_context: The dialog context for the current turn of conversation.
        :param options: (Optional) additional argument(s) to pass to the dialog being started.
        """
        raise NotImplementedError()

    async def continue_dialog(self, dialog_context: "DialogContext"):
        """
        Method called when an instance of the dialog is the "current" dialog and the
        user replies with a new activity. The dialog will generally continue to receive the user's
        replies until it calls either `end_dialog()` or `begin_dialog()`.
        If this method is NOT implemented then the dialog will automatically be ended when the user replies.
        :param dialog_context: The dialog context for the current turn of conversation.
        :return:
        """
        # By default just end the current dialog.
        return await dialog_context.end_dialog(None)

    async def resume_dialog(  # pylint: disable=unused-argument
        self, dialog_context: "DialogContext", reason: DialogReason, result: object
    ):
        """
        Method called when an instance of the dialog is being returned to from another
        dialog that was started by the current instance using `begin_dialog()`.
        If this method is NOT implemented then the dialog will be automatically ended with a call
        to `end_dialog()`. Any result passed from the called dialog will be passed
        to the current dialog's parent.
        :param dialog_context: The dialog context for the current turn of conversation.
        :param reason: Reason why the dialog resumed.
        :param result: (Optional) value returned from the dialog that was called. The type of the value returned is
        dependent on the dialog that was called.
        :return:
        """
        # By default just end the current dialog and return result to parent.
        return await dialog_context.end_dialog(result)

    # TODO: instance is DialogInstance
    async def reprompt_dialog(  # pylint: disable=unused-argument
        self, context: TurnContext, instance: DialogInstance
    ):
        """
        :param context:
        :param instance:
        :return:
        """
        # No-op by default
        return

    # TODO: instance is DialogInstance
    async def end_dialog(  # pylint: disable=unused-argument
        self, context: TurnContext, instance: DialogInstance, reason: DialogReason
    ):
        """
        :param context:
        :param instance:
        :param reason:
        :return:
        """
        # No-op by default
        return
