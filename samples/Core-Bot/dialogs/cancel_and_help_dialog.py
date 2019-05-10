# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import ComponentDialog, DialogContext, DialogTurnResult, DialogTurnStatus
from botbuilder.schema import ActivityTypes


class CancelAndHelpDialog(ComponentDialog):

    def __init__(self, dialog_id: str):
        super(CancelAndHelpDialog, self).__init__(dialog_id)
    
    async def on_begin_dialog(self, inner_dc: DialogContext, options: object) -> DialogTurnResult:
        result = await self.interrupt(inner_dc)
        if result is not None:
            return result

        return await super(CancelAndHelpDialog, self).on_begin_dialog(inner_dc, options)
    
    async def on_continue_dialog(self, inner_dc: DialogContext) -> DialogTurnResult:
        result = await self.interrupt(inner_dc)
        if result is not None:
            return result

        return await super(CancelAndHelpDialog, self).on_continue_dialog(inner_dc)

    async def interrupt(self, inner_dc: DialogContext) -> DialogTurnResult:
        if inner_dc.context.activity.type == ActivityTypes.message:
            text = inner_dc.context.activity.text.lower()

            if text == 'help' or text == '?':
                await inner_dc.context.send_activity("Show Help...")
                return DialogTurnResult(DialogTurnStatus.Waiting)

            if text == 'cancel' or text == 'quit':
                await inner_dc.context.send_activity("Cancelling")
                return await inner_dc.cancel_all_dialogs()

        return None