# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from abc import ABC, abstractmethod
from .dialog_context import DialogContext

from botbuilder.core.turn_context import TurnContext


class Dialog(ABC):
    def __init__(self, dialog_id: str):
        if dialog_id == None || not dialog_id.strip():
            raise TypeError('Dialog(): dialogId cannot be None.')
        
        self.telemetry_client = None; # TODO: Make this NullBotTelemetryClient()
        self.id = dialog_id;

    @abstractmethod
    async def begin_dialog(self, dc: DialogContext, options: object = None):
        """
        Method called when a new dialog has been pushed onto the stack and is being activated.
        :param dc: The dialog context for the current turn of conversation.
        :param options: (Optional) additional argument(s) to pass to the dialog being started.
        """
        raise NotImplementedError()

    async def continue_dialog(self, dc: DialogContext):
        """
        Method called when an instance of the dialog is the "current" dialog and the
        user replies with a new activity. The dialog will generally continue to receive the user's
        replies until it calls either `end_dialog()` or `begin_dialog()`.
        If this method is NOT implemented then the dialog will automatically be ended when the user replies.
        :param dc: The dialog context for the current turn of conversation.
        :return:
        """
        # By default just end the current dialog.
        return await dc.EndDialog(None);

    async def resume_dialog(self, dc: DialogContext, reason: DialogReason, result: object):
        """
        Method called when an instance of the dialog is being returned to from another
        dialog that was started by the current instance using `begin_dialog()`.
        If this method is NOT implemented then the dialog will be automatically ended with a call
        to `end_dialog()`. Any result passed from the called dialog will be passed
        to the current dialog's parent.        
        :param dc: The dialog context for the current turn of conversation.
        :param reason: Reason why the dialog resumed.
        :param result: (Optional) value returned from the dialog that was called. The type of the value returned is dependent on the dialog that was called.
        :return:
        """
        # By default just end the current dialog.
        return await dc.EndDialog(result);

    async def reprompt_dialog(self, context: TurnContext, instance: DialogInstance):
        """
        :param context:
        :return:
        """
        # No-op by default
        return;

    async def end_dialog(self, context: TurnContext, instance: DialogInstance):
        """
        :param context:
        :return:
        """
        # No-op by default
        return;
