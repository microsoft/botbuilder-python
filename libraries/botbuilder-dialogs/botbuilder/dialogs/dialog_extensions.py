# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import BotAdapter, StatePropertyAccessor, TurnContext
from botbuilder.dialogs import (
    Dialog,
    DialogContext,
    DialogEvents,
    DialogSet,
    DialogTurnStatus,
)
from botbuilder.schema import Activity, ActivityTypes
from botframework.connector.auth import ClaimsIdentity, SkillValidation


class DialogExtensions:
    @staticmethod
    async def run_dialog(
        dialog: Dialog, turn_context: TurnContext, accessor: StatePropertyAccessor
    ):
        dialog_set = DialogSet(accessor)
        dialog_set.add(dialog)

        dialog_context = await dialog_set.create_context(turn_context)

        claims = turn_context.turn_state.get(BotAdapter.BOT_IDENTITY_KEY)
        if isinstance(claims, ClaimsIdentity) and SkillValidation.is_skill_claim(
            claims.claims
        ):
            # The bot is running as a skill.
            if (
                turn_context.activity.type == ActivityTypes.end_of_conversation
                and dialog_context.stack
            ):
                await dialog_context.cancel_all_dialogs()
            else:
                # Process a reprompt event sent from the parent.
                if (
                    turn_context.activity.type == ActivityTypes.event
                    or turn_context.activity.name == DialogEvents.reprompt_dialog
                    and dialog_context.stack
                ):
                    await dialog.reprompt_dialog()
                    return

                # Run the Dialog with the new message Activity and capture the results
                # so we can send end of conversation if needed.
                result = await dialog_context.continue_dialog()
                if result.status == DialogTurnStatus.Empty:
                    start_message_text = f"Starting {dialog.id}"
                    await turn_context.send_trace_activity(
                        f"Extension {Dialog.__name__}.run_dialog",
                        label=start_message_text,
                    )
                    result = await dialog_context.begin_dialog(dialog.id)

                # Send end of conversation if it is completed or cancelled.
                if (
                    result.status == DialogTurnStatus.Complete
                    or result.status == DialogTurnStatus.Cancelled
                ):
                    end_message_text = f"Dialog {dialog.id} has **completed**. Sending EndOfConversation."
                    await turn_context.send_trace_activity(
                        f"Extension {Dialog.__name__}.run_dialog",
                        label=end_message_text,
                        value=result.result,
                    )

                    activity = Activity(
                        type=ActivityTypes.end_of_conversation, value=result.result
                    )
                    await turn_context.send_activity(activity)

        else:
            # The bot is running as a standard bot.
            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                await dialog_context.begin_dialog(dialog.id)

    @staticmethod
    async def _get_active_dialog_context(dialog_context: DialogContext):
        child = dialog_context.child
