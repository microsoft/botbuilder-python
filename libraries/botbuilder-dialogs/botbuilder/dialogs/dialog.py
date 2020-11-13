# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from abc import ABC, abstractmethod

from botbuilder.core import TurnContext, NullTelemetryClient, BotTelemetryClient
from .dialog_reason import DialogReason
from .dialog_event import DialogEvent
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

    def get_version(self) -> str:
        return self.id

    async def on_dialog_event(
        self, dialog_context: "DialogContext", dialog_event: DialogEvent
    ) -> bool:
        """
        Called when an event has been raised, using `DialogContext.emitEvent()`, by either the current dialog or a
         dialog that the current dialog started.
        :param dialog_context: The dialog context for the current turn of conversation.
        :param dialog_event: The event being raised.
        :return: True if the event is handled by the current dialog and bubbling should stop.
        """
        # Before bubble
        handled = await self._on_pre_bubble_event(dialog_context, dialog_event)

        # Bubble as needed
        if (not handled) and dialog_event.bubble and dialog_context.parent:
            handled = await dialog_context.parent.emit(
                dialog_event.name, dialog_event.value, True, False
            )

        # Post bubble
        if not handled:
            handled = await self._on_post_bubble_event(dialog_context, dialog_event)

        return handled

    async def _on_pre_bubble_event(  # pylint: disable=unused-argument
        self, dialog_context: "DialogContext", dialog_event: DialogEvent
    ) -> bool:
        """
        Called before an event is bubbled to its parent.
        This is a good place to perform interception of an event as returning `true` will prevent
        any further bubbling of the event to the dialogs parents and will also prevent any child
        dialogs from performing their default processing.
        :param dialog_context: The dialog context for the current turn of conversation.
        :param dialog_event: The event being raised.
        :return: Whether the event is handled by the current dialog and further processing should stop.
        """
        return False

    async def _on_post_bubble_event(  # pylint: disable=unused-argument
        self, dialog_context: "DialogContext", dialog_event: DialogEvent
    ) -> bool:
        """
        Called after an event was bubbled to all parents and wasn't handled.
        This is a good place to perform default processing logic for an event. Returning `true` will
        prevent any processing of the event by child dialogs.
        :param dialog_context: The dialog context for the current turn of conversation.
        :param dialog_event: The event being raised.
        :return: Whether the event is handled by the current dialog and further processing should stop.
        """
        return False

    def _on_compute_id(self) -> str:
        """
        Computes an unique ID for a dialog.
        :return: An unique ID for a dialog
        """
        return self.__class__.__name__

    def _register_source_location(
        self, path: str, line_number: int
    ):  # pylint: disable=unused-argument
        """
        Registers a SourceRange in the provided location.
        :param path: The path to the source file.
        :param line_number: The line number where the source will be located on the file.
        :return:
        """
        if path:
            # This will be added when debbuging support is ported.
            # DebugSupport.source_map.add(self, SourceRange(
            #     path = path,
            #     start_point = SourcePoint(line_index = line_number, char_index = 0 ),
            #     end_point = SourcePoint(line_index = line_number + 1, char_index = 0 ),
            # )
            return
