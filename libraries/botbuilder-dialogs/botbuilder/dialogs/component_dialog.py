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
    """
    A :class:`Dialog` that is composed of other dialogs
    
    A component dialog has an inner :class:`DialogSet` :class:`DialogContext`,
    which provides an inner dialog stack that is hidden from the parent dialog.
    
    :var persisted_dialog state:
    :vartype persisted_dialog_state: str
    """
    persisted_dialog_state = "dialogs"

    def __init__(self, dialog_id: str):
        """
        Initializes a new instance of the :class:`ComponentDialog`

        :param dialog_id: The ID to assign to the new dialog within the parent dialog set.
        :type dialog_id: str
        """
        super(ComponentDialog, self).__init__(dialog_id)

        if dialog_id is None:
            raise TypeError("ComponentDialog(): dialog_id cannot be None.")

        self._dialogs = DialogSet()
        self.initial_dialog_id = None

    # TODO: Add TelemetryClient

    async def begin_dialog(
        self, dialog_context: DialogContext, options: object = None
    ) -> DialogTurnResult:
        """
        Called when the dialog is started and pushed onto the parent's dialog stack.
        
        If the task is successful, the result indicates whether the dialog is still
        active after the turn has been processed by the dialog.

        :param dialog_context: The :class:`DialogContext` for the current turn of the conversation.
        :type dialog_context: :class:`DialogContext`
        :param options: Optional, initial information to pass to the dialog.
        :type options: object
        :return: Signals the end of the turn
        :rtype: :class:`Dialog.end_of_turn`
        """
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
        """
        Called when the dialog is continued, where it is the active dialog and the
        user replies with a new activity.

        .. note::
            If the task is successful, the result indicates whether the dialog is still
            active after the turn has been processed by the dialog. The result may also
            contain a return value.

            If this method is *not* overriden the component dialog calls the 
            :meth:`DialogContext.continue_dialog` method on it's inner dialog
            context. If the inner dialog stack is empty, the component dialog ends,
            and if a :class:`DialogTurnResult.result` is available, the component dialog
            uses that as it's return value.


        :param dialog_context: The parent :class:`DialogContext` for the current turn of the conversation.
        :type dialog_context: :class:`DialogContext`
        :return: Signals the end of the turn
        :rtype: :class:`Dialog.end_of_turn`
        """
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
        """
        Called when a child dialog on the parent's dialog stack completed this turn, returning
        control to this dialog component.

        .. note::
            If the task is successful, the result indicates whether this dialog is still
            active after this dialog turn has been processed.

            Generally, the child dialog was started with a call to :meth:`def async begin_dialog()`
            in the parent's context. However, if the :meth:`DialogContext.replace_dialog()` method is
            is called, the logical child dialog may be different than the original.

            If this method is *not* overridden, the dialog automatically calls its
            :meth:`asyn def reprompt_dialog()` when the user replies. 

        :param dialog_context: The :class:`DialogContext` for the current turn of the conversation.
        :type dialog_context: :class:`DialogContext`
        :param reason: Reason why the dialog resumed.
        :type reason: :class:`DialogReason`
        :param result: Optional, value returned from the dialog that was called. The type of the value returned is dependent on the child dialog.
        :type result: object
        :return: Signals the end of the turn
        :rtype: :class:`Dialog.end_of_turn`
        """

        """ 
        Containers are typically leaf nodes on the stack but the dev is free to push other dialogs
        on top of the stack which will result in the container receiving an unexpected call to
        resume_dialog() when the pushed on dialog ends.
        To avoid the container prematurely ending we need to implement this method and simply
        ask our inner dialog stack to re-prompt.
        """
        await self.reprompt_dialog(dialog_context.context, dialog_context.active_dialog)
        return Dialog.end_of_turn

    async def reprompt_dialog(
        self, context: TurnContext, instance: DialogInstance
    ) -> None:
        """
        Called when the dialog should re-prompt the user for input.

        :param context: The context object for this turn.
        :type context: :class:`TurnContext`
        :param instance: State information for this dialog.
        :type instance: :class:`DialogInstance`
        """
        # Delegate to inner dialog.
        dialog_state = instance.state[self.persisted_dialog_state]
        inner_dc = DialogContext(self._dialogs, context, dialog_state)
        await inner_dc.reprompt_dialog()

        # Notify component
        await self.on_reprompt_dialog(context, instance)

    async def end_dialog(
        self, context: TurnContext, instance: DialogInstance, reason: DialogReason
    ) -> None:
        """
        Called when the dialog is ending.

        :param context: The context object for this turn.
        :type context: :class:`TurnContext`
        :param instance: State information associated with the instance of this component dialog on its parent's dialog stack.
        :type instance: :class:`DialogInstance`
        :param reason: Reason why the dialog ended.
        :type reason: :class:`DialogReason`
        """
        # Forward cancel to inner dialog
        if reason == DialogReason.CancelCalled:
            dialog_state = instance.state[self.persisted_dialog_state]
            inner_dc = DialogContext(self._dialogs, context, dialog_state)
            await inner_dc.cancel_all_dialogs()
        await self.on_end_dialog(context, instance, reason)

    def add_dialog(self, dialog: Dialog) -> object:
        """
        Adds a :class:`Dialog` to the component dialog and returns the updated component.
        Adding a new dialog will inherit the :class:`BotTelemetryClient` of the :class:`ComponentDialog`.
        
        :param dialog: The dialog to add.
        :return: The updated :class:`ComponentDialog`
        :rtype: :class:`ComponentDialog`
        """
        self._dialogs.add(dialog)
        if not self.initial_dialog_id:
            self.initial_dialog_id = dialog.id
        return self

    def find_dialog(self, dialog_id: str) -> Dialog:
        """
        Finds a dialog by ID.
        Adding a new dialog will inherit the :class:`BotTelemetryClient` of the :class:`ComponentDialog`.
        
        :param dialog_id: The dialog to add.
        :return: The dialog; or None if there is not a match for the ID.
        :rtype: :class:Dialog
        """
        return self._dialogs.find(dialog_id)

    async def on_begin_dialog(
        self, inner_dc: DialogContext, options: object
    ) -> DialogTurnResult:
        """
        Called when the dialog is started and pushed onto the parent's dialog stack.

        .. note::

            If the task is successful, the result indicates whether the dialog is still
            active after the turn has been processed by the dialog.

            By default, this calls the :meth:`Dialog.begin_dialog()` method of the component
            dialog's initial dialog.

            Override this method in a derived class to implement interrupt logic.

        :param inner_dc: The inner :class:`DialogContext` for the current turn of conversation.
        :type inner_dc: :class:`DialogContext`
        :param options: Optional, initial information to pass to the dialog.
        :type options: object
        :return: ?
        :rtype: ?
        """
        return await inner_dc.begin_dialog(self.initial_dialog_id, options)

    async def on_continue_dialog(self, inner_dc: DialogContext) -> DialogTurnResult:
        return await inner_dc.continue_dialog()

    async def on_end_dialog(  # pylint: disable=unused-argument
        self, context: TurnContext, instance: DialogInstance, reason: DialogReason
    ) -> None:
        """
        Ends the component dialog in its parent's context.

        :param turn_context: The :class:`TurnContext` for the current turn of the conversation.
        :type turn_context: :class:`TurnContext`
        :param instance: State information associated with the instance of this component dialog on its parent's dialog stack.
        :type instance: :class:`DialogInstance`
        :param reason: Reason why the dialog ended.
        :type reason: :class:`DialogReason`
        """
        return

    async def on_reprompt_dialog(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, instance: DialogInstance
    ) -> None:
        """
        :param turn_context: The :class:`TurnContext` for the current turn of the conversation.
        :type turn_context: :class:`DialogInstance`
        :param instance: State information associated with the instance of this component dialog on its parent's dialog stack.
        :type instance: :class:`DialogInstance`
        """
        return

    async def end_component(
        self, outer_dc: DialogContext, result: object  # pylint: disable=unused-argument
    ) -> DialogTurnResult:
        """
        Ends the component dialog in its parent's context.
        .. note::
            If the task is successful, the result indicates that the dialog ended after the
            turn was processed by the dialog.

            In general, the parent context is the dialog or bot turn handler that started the dialog.
            If the parent is a dialog, the stack calls the parent's :meth:`Dialog.resume_dialog()` method
            to return a result to the parent dialog. If the parent dialog does not implement
            :meth:`Dialog.resume_dialog()`, then the parent will end, too, and the result is passed to the next
            parent context, if one exists.

            The returned :class:`DialogTurnResult`contains the return value in its
            :class:`DialogTurnResult.result` property.

        :param outer_dc: The parent class:`DialogContext` for the current turn of conversation.
        :type outer_dc: class:`DialogContext`
        :param result: Optional, value to return from the dialog component to the parent context.
        :type result: object
        :return: Value to return.
        :rtype: :class:`DialogTurnResult.result`
        """
        return await outer_dc.end_dialog(result)
