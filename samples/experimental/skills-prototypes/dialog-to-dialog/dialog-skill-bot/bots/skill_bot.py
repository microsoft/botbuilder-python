# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import platform

from botbuilder.core import Bot, ConversationState, MessageFactory, TurnContext
from botbuilder.dialogs import Dialog, DialogContext, DialogSet, DialogTurnStatus
from botbuilder.schema import Activity, ActivityTypes, InputHints


class SkillBot(Bot):
    def __init__(self, conversation_state: ConversationState, main_dialog: Dialog):
        self._conversation_state = conversation_state
        self._main_dialog = main_dialog

    async def on_turn(self, context: TurnContext):
        dialog_set = DialogSet(self._conversation_state.create_property("DialogState"))
        dialog_set.add(self._main_dialog)

        dialog_context = await dialog_set.create_context(context)
        if context.activity.type == ActivityTypes.end_of_conversation and dialog_context.stack:
            # Handle remote cancellation request if we have something in the stack.
            active_dialog_context = self._get_active_dialog_context(dialog_context)

            # Send cancellation message to the top dialog in the stack to ensure all the
            # parents are canceled in the right order.
            await active_dialog_context.cancel_all_dialogs()
            remote_cancel_text = "**SkillBot.** The current mainDialog in the skill was **canceled** by a " \
                                 "request **from the host**, do some cleanup here if needed."
            await context.send_activity(MessageFactory.text(remote_cancel_text, input_hint=InputHints.ignoring_input))
        else:
            # Run the Dialog with the new message Activity and capture the results so we can send end of
            # conversation if needed.
            result = await dialog_context.continue_dialog()
            if result.status == DialogTurnStatus.Empty:
                start_message_text = f"**SkillBot.** Starting {self._main_dialog.id} " \
                    f"(Pyhton {platform.python_version()})."

                await context.send_activity(MessageFactory.text(
                    start_message_text,
                    input_hint=InputHints.ignoring_input
                ))
                result = await dialog_context.begin_dialog(self._main_dialog.id)

            # Send end of conversation if it is complete
            if result.status == DialogTurnStatus.Complete or result.status == DialogTurnStatus.Cancelled:
                end_message_text = "**SkillBot.** The mainDialog in the skill has **completed**. " \
                                   "Sending EndOfConversation."
                await context.send_activity(MessageFactory.text(
                    end_message_text,
                    input_hint=InputHints.ignoring_input
                ))

                activity = Activity(type=ActivityTypes.end_of_conversation, value=result.result)
                await context.send_activity(activity)

        # Save any state changes that might have happened during the turn.
        await self._conversation_state.save_changes(context, False)



    def _get_active_dialog_context(self, dialog_context: DialogContext) -> DialogContext:
        # Check non adaptive version of this method
        raise NotImplementedError()
