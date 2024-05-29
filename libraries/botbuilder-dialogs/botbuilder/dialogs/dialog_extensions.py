# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botframework.connector.auth import (
    ClaimsIdentity,
    SkillValidation,
    AuthenticationConstants,
    GovernmentConstants,
)
from botbuilder.core import BotAdapter, StatePropertyAccessor, TurnContext
from botbuilder.core.skills import SkillHandler, SkillConversationReference
import botbuilder.dialogs as dialogs  # pylint: disable=unused-import
from botbuilder.dialogs.memory import DialogStateManager
from botbuilder.dialogs.dialog_context import DialogContext
from botbuilder.dialogs.dialog_turn_result import DialogTurnResult
from botbuilder.dialogs import (
    DialogEvents,
    DialogSet,
    DialogTurnStatus,
)
from botbuilder.schema import Activity, ActivityTypes, EndOfConversationCodes


class DialogExtensions:
    @staticmethod
    async def run_dialog(
        dialog: "dialogs.Dialog",
        turn_context: TurnContext,
        accessor: StatePropertyAccessor,
    ):
        """
        Creates a dialog stack and starts a dialog, pushing it onto the stack.
        """

        dialog_set = DialogSet(accessor)
        dialog_set.add(dialog)

        dialog_context: DialogContext = await dialog_set.create_context(turn_context)

        await DialogExtensions._internal_run(turn_context, dialog.id, dialog_context)

    @staticmethod
    async def _internal_run(
        context: TurnContext, dialog_id: str, dialog_context: DialogContext
    ) -> DialogTurnResult:
        # map TurnState into root dialog context.services
        for key, service in context.turn_state.items():
            dialog_context.services[key] = service

        # get the DialogStateManager configuration
        dialog_state_manager = DialogStateManager(dialog_context)
        await dialog_state_manager.load_all_scopes()
        dialog_context.context.turn_state[dialog_state_manager.__class__.__name__] = (
            dialog_state_manager
        )

        # Loop as long as we are getting valid OnError handled we should continue executing the actions for the turn.

        # NOTE: We loop around this block because each pass through we either complete the turn and break out of the
        # loop or we have had an exception AND there was an OnError action which captured the error.  We need to
        # continue the turn based on the actions the OnError handler introduced.
        end_of_turn = False
        while not end_of_turn:
            try:
                dialog_turn_result = await DialogExtensions.__inner_run(
                    context, dialog_id, dialog_context
                )

                # turn successfully completed, break the loop
                end_of_turn = True
            except Exception as err:
                # fire error event, bubbling from the leaf.
                handled = await dialog_context.emit_event(
                    DialogEvents.error, err, bubble=True, from_leaf=True
                )

                if not handled:
                    # error was NOT handled, throw the exception and end the turn. (This will trigger the
                    # Adapter.OnError handler and end the entire dialog stack)
                    raise

        # save all state scopes to their respective botState locations.
        await dialog_state_manager.save_all_changes()

        # return the redundant result because the DialogManager contract expects it
        return dialog_turn_result

    @staticmethod
    async def __inner_run(
        turn_context: TurnContext, dialog_id: str, dialog_context: DialogContext
    ) -> DialogTurnResult:
        # Handle EoC and Reprompt event from a parent bot (can be root bot to skill or skill to skill)
        if DialogExtensions.__is_from_parent_to_skill(turn_context):
            # Handle remote cancellation request from parent.
            if turn_context.activity.type == ActivityTypes.end_of_conversation:
                if not dialog_context.stack:
                    # No dialogs to cancel, just return.
                    return DialogTurnResult(DialogTurnStatus.Empty)

                # Send cancellation message to the dialog to ensure all the parents are canceled
                # in the right order.
                return await dialog_context.cancel_all_dialogs(True)

            # Handle a reprompt event sent from the parent.
            if (
                turn_context.activity.type == ActivityTypes.event
                and turn_context.activity.name == DialogEvents.reprompt_dialog
            ):
                if not dialog_context.stack:
                    # No dialogs to reprompt, just return.
                    return DialogTurnResult(DialogTurnStatus.Empty)

                await dialog_context.reprompt_dialog()
                return DialogTurnResult(DialogTurnStatus.Waiting)

        # Continue or start the dialog.
        result = await dialog_context.continue_dialog()
        if result.status == DialogTurnStatus.Empty:
            result = await dialog_context.begin_dialog(dialog_id)

        await DialogExtensions._send_state_snapshot_trace(dialog_context)

        # Skills should send EoC when the dialog completes.
        if (
            result.status == DialogTurnStatus.Complete
            or result.status == DialogTurnStatus.Cancelled
        ):
            if DialogExtensions.__send_eoc_to_parent(turn_context):
                activity = Activity(
                    type=ActivityTypes.end_of_conversation,
                    value=result.result,
                    locale=turn_context.activity.locale,
                    code=(
                        EndOfConversationCodes.completed_successfully
                        if result.status == DialogTurnStatus.Complete
                        else EndOfConversationCodes.user_cancelled
                    ),
                )
                await turn_context.send_activity(activity)

        return result

    @staticmethod
    def __is_from_parent_to_skill(turn_context: TurnContext) -> bool:
        if turn_context.turn_state.get(SkillHandler.SKILL_CONVERSATION_REFERENCE_KEY):
            return False

        claims_identity = turn_context.turn_state.get(BotAdapter.BOT_IDENTITY_KEY)
        return isinstance(
            claims_identity, ClaimsIdentity
        ) and SkillValidation.is_skill_claim(claims_identity.claims)

    @staticmethod
    async def _send_state_snapshot_trace(dialog_context: DialogContext):
        """
        Helper to send a trace activity with a memory snapshot of the active dialog DC.
        :param dialog_context:
        :return:
        """
        claims_identity = dialog_context.context.turn_state.get(
            BotAdapter.BOT_IDENTITY_KEY, None
        )
        trace_label = (
            "Skill State"
            if isinstance(claims_identity, ClaimsIdentity)
            and SkillValidation.is_skill_claim(claims_identity.claims)
            else "Bot State"
        )
        # send trace of memory
        snapshot = DialogExtensions._get_active_dialog_context(
            dialog_context
        ).state.get_memory_snapshot()
        trace_activity = Activity.create_trace_activity(
            "BotState",
            "https://www.botframework.com/schemas/botState",
            snapshot,
            trace_label,
        )
        await dialog_context.context.send_activity(trace_activity)

    @staticmethod
    def __send_eoc_to_parent(turn_context: TurnContext) -> bool:
        claims_identity = turn_context.turn_state.get(BotAdapter.BOT_IDENTITY_KEY)
        if isinstance(
            claims_identity, ClaimsIdentity
        ) and SkillValidation.is_skill_claim(claims_identity.claims):
            # EoC Activities returned by skills are bounced back to the bot by SkillHandler.
            # In those cases we will have a SkillConversationReference instance in state.
            skill_conversation_reference: SkillConversationReference = (
                turn_context.turn_state.get(
                    SkillHandler.SKILL_CONVERSATION_REFERENCE_KEY
                )
            )
            if skill_conversation_reference:
                # If the skillConversationReference.OAuthScope is for one of the supported channels,
                # we are at the root and we should not send an EoC.
                return (
                    skill_conversation_reference.oauth_scope
                    != AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
                    and skill_conversation_reference.oauth_scope
                    != GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
                )
            return True

        return False

    @staticmethod
    def _get_active_dialog_context(dialog_context: DialogContext) -> DialogContext:
        """
        Recursively walk up the DC stack to find the active DC.
        :param dialog_context:
        :return:
        """
        child = dialog_context.child
        if not child:
            return dialog_context

        return DialogExtensions._get_active_dialog_context(child)
