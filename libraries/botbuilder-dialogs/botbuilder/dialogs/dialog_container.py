# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod


from botbuilder.core import NullTelemetryClient, BotTelemetryClient
from .dialog import Dialog
from .dialog_context import DialogContext
from .dialog_event import DialogEvent
from .dialog_events import DialogEvents
from .dialog_set import DialogSet


class DialogContainer(Dialog, ABC):
    def __init__(self, dialog_id: str = None):
        super().__init__(dialog_id)

        self.dialogs = DialogSet()

    @property
    def telemetry_client(self) -> BotTelemetryClient:
        """
        Gets the telemetry client for logging events.
        """
        return self._telemetry_client

    @telemetry_client.setter
    def telemetry_client(self, value: BotTelemetryClient) -> None:
        """
        Sets the telemetry client for all dialogs in this set.
        """
        if value is None:
            self._telemetry_client = NullTelemetryClient()
        else:
            self._telemetry_client = value

        # Care! Dialogs.TelemetryClient assignment internally assigns the
        # TelemetryClient for each dialog which could lead to an eventual stack
        # overflow in cyclical dialog structures.
        # Don't set the telemetry client if the candidate instance is the same as
        # the currently set one.
        if self.dialogs.telemetry_client != value:
            self.dialogs.telemetry_client = self._telemetry_client

    @abstractmethod
    def create_child_context(self, dialog_context: DialogContext) -> DialogContext:
        raise NotImplementedError()

    def find_dialog(self, dialog_id: str) -> Dialog:
        # TODO: deprecate DialogSet.find
        return self.dialogs.find_dialog(dialog_id)

    async def on_dialog_event(
        self, dialog_context: DialogContext, dialog_event: DialogEvent
    ) -> bool:
        """
        Called when an event has been raised, using `DialogContext.emitEvent()`, by either the current dialog or a
         dialog that the current dialog started.
        :param dialog_context: The dialog context for the current turn of conversation.
        :param dialog_event: The event being raised.
        :return: True if the event is handled by the current dialog and bubbling should stop.
        """
        handled = await super().on_dialog_event(dialog_context, dialog_event)

        # Trace unhandled "versionChanged" events.
        if not handled and dialog_event.name == DialogEvents.version_changed:
            trace_message = (
                f"Unhandled dialog event: {dialog_event.name}. Active Dialog: "
                f"{dialog_context.active_dialog.id}"
            )

            await dialog_context.context.send_trace_activity(trace_message)

        return handled

    def get_internal_version(self) -> str:
        """
        GetInternalVersion - Returns internal version identifier for this container.
        DialogContainers detect changes of all sub-components in the container and map that to an DialogChanged event.
        Because they do this, DialogContainers "hide" the internal changes and just have the .id. This isolates changes
        to the container level unless a container doesn't handle it.  To support this DialogContainers define a
        protected virtual method GetInternalVersion() which computes if this dialog or child dialogs have changed
        which is then examined via calls to check_for_version_change_async().
        :return: version which represents the change of the internals of this container.
        """
        return self.dialogs.get_version()

    async def check_for_version_change_async(self, dialog_context: DialogContext):
        """
        :param dialog_context: dialog context.
        :return: task.
        Checks to see if a containers child dialogs have changed since the current dialog instance
        was started.

        This should be called at the start of `beginDialog()`, `continueDialog()`, and `resumeDialog()`.
        """
        current = dialog_context.active_dialog.version
        dialog_context.active_dialog.version = self.get_internal_version()

        # Check for change of previously stored hash
        if current and current != dialog_context.active_dialog.version:
            # Give bot an opportunity to handle the change.
            # - If bot handles it the changeHash will have been updated as to avoid triggering the
            #   change again.
            await dialog_context.emit_event(
                DialogEvents.version_changed, self.id, True, False
            )
