# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


from botbuilder.core import TurnContext
from .dialog import Dialog
from .dialog_context import DialogContext
from .dialog_turn_result import DialogTurnResult
from .dialog_state import DialogState
from .dialog_turn_status import DialogTurnStatus
from .dialog_reason import DialogReason
from .dialog_set import DialogSet
from .dialog_instance import DialogInstance


class ComponentDialog(Dialog):
    persisted_dialog_state = "dialogs"

    def __init__(self, dialog_id: str):
        super(ComponentDialog, self).__init__(dialog_id)

        if dialog_id is None:
            raise TypeError("ComponentDialog(): dialog_id cannot be None.")

        self._dialogs = DialogSet()
        self.initial_dialog_id = None

    # TODO: Add TelemetryClient

    async def begin_dialog(
        self, dialog_context: DialogContext, options: object = None
    ) -> DialogTurnResult:
        if dialog_context is None:
            raise TypeError("ComponentDialog.begin_dialog(): outer_dc cannot be None.")

        # Start the inner dialog.
        dialog_state = DialogState()
        dialog_context.active_dialog.state[self.persisted_dialog_state] = dialog_state
        inner_dc = DialogContext(self._dialogs, dialog_context.context, dialog_state)
        inner_dc.parent = dialog_context
        turn_result = await self.on_begin_dialog(inner_dc, options)

        # Check for end of inner dialog
        if turn_result.status != DialogTurnStatus.Waiting:
            # Return result to calling dialog
            return await self.end_component(dialog_context, turn_result.result)

        # Just signal waiting
        return Dialog.end_of_turn

    async def continue_dialog(self, dialog_context: DialogContext) -> DialogTurnResult:
        if dialog_context is None:
            raise TypeError("ComponentDialog.begin_dialog(): outer_dc cannot be None.")
        # Continue execution of inner dialog.
        dialog_state = dialog_context.active_dialog.state[self.persisted_dialog_state]
        inner_dc = DialogContext(self._dialogs, dialog_context.context, dialog_state)
        inner_dc.parent = dialog_context
        turn_result = await self.on_continue_dialog(inner_dc)

        if turn_result.status != DialogTurnStatus.Waiting:
            return await self.end_component(dialog_context, turn_result.result)

        return Dialog.end_of_turn

    async def resume_dialog(
        self, dialog_context: DialogContext, reason: DialogReason, result: object = None
    ) -> DialogTurnResult:
        # Containers are typically leaf nodes on the stack but the dev is free to push other dialogs
        # on top of the stack which will result in the container receiving an unexpected call to
        # resume_dialog() when the pushed on dialog ends.
        # To avoid the container prematurely ending we need to implement this method and simply
        # ask our inner dialog stack to re-prompt.
        await self.reprompt_dialog(dialog_context.context, dialog_context.active_dialog)
        return Dialog.end_of_turn

    async def reprompt_dialog(
        self, context: TurnContext, instance: DialogInstance
    ) -> None:
        # Delegate to inner dialog.
        dialog_state = instance.state[self.persisted_dialog_state]
        inner_dc = DialogContext(self._dialogs, context, dialog_state)
        await inner_dc.reprompt_dialog()

        # Notify component
        await self.on_reprompt_dialog(context, instance)

    async def end_dialog(
        self, context: TurnContext, instance: DialogInstance, reason: DialogReason
    ) -> None:
        # Forward cancel to inner dialogs
        if reason == DialogReason.CancelCalled:
            dialog_state = instance.state[self.persisted_dialog_state]
            inner_dc = DialogContext(self._dialogs, context, dialog_state)
            await inner_dc.cancel_all_dialogs()
        await self.on_end_dialog(context, instance, reason)

    def add_dialog(self, dialog: Dialog) -> object:
        """
        Adds a dialog to the component dialog.
        Adding a new dialog will inherit the BotTelemetryClient of the ComponentDialog.
        :param dialog: The dialog to add.
        :return: The updated ComponentDialog
        """
        self._dialogs.add(dialog)
        if not self.initial_dialog_id:
            self.initial_dialog_id = dialog.id
        return self

    def find_dialog(self, dialog_id: str) -> Dialog:
        """
        Finds a dialog by ID.
        Adding a new dialog will inherit the BotTelemetryClient of the ComponentDialog.
        :param dialog_id: The dialog to add.
        :return: The dialog; or None if there is not a match for the ID.
        """
        return self._dialogs.find(dialog_id)

    async def on_begin_dialog(
        self, inner_dc: DialogContext, options: object
    ) -> DialogTurnResult:
        return await inner_dc.begin_dialog(self.initial_dialog_id, options)

    async def on_continue_dialog(self, inner_dc: DialogContext) -> DialogTurnResult:
        return await inner_dc.continue_dialog()

    async def on_end_dialog(  # pylint: disable=unused-argument
        self, context: TurnContext, instance: DialogInstance, reason: DialogReason
    ) -> None:
        return

    async def on_reprompt_dialog(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, instance: DialogInstance
    ) -> None:
        return

    async def end_component(
        self, outer_dc: DialogContext, result: object  # pylint: disable=unused-argument
    ) -> DialogTurnResult:
        return await outer_dc.end_dialog(result)
