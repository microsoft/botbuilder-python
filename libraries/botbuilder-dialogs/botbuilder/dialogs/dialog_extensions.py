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
from botbuilder.dialogs import (
    Dialog,
    DialogEvents,
    DialogSet,
    DialogTurnStatus,
)
from botbuilder.schema import Activity, ActivityTypes, EndOfConversationCodes


class DialogExtensions:
    @staticmethod
    async def run_dialog(
        dialog: Dialog, turn_context: TurnContext, accessor: StatePropertyAccessor
    ):
        """
        Creates a dialog stack and starts a dialog, pushing it onto the stack.
        """

        dialog_set = DialogSet(accessor)
        dialog_set.add(dialog)

        dialog_context = await dialog_set.create_context(turn_context)

        # Handle EoC and Reprompt event from a parent bot (can be root bot to skill or skill to skill)
        if DialogExtensions.__is_from_parent_to_skill(turn_context):
            # Handle remote cancellation request from parent.
            if turn_context.activity.type == ActivityTypes.end_of_conversation:
                if not dialog_context.stack:
                    # No dialogs to cancel, just return.
                    return

                # Send cancellation message to the dialog to ensure all the parents are canceled
                # in the right order.
                await dialog_context.cancel_all_dialogs()
                return

            # Handle a reprompt event sent from the parent.
            if (
                turn_context.activity.type == ActivityTypes.event
                and turn_context.activity.name == DialogEvents.reprompt_dialog
            ):
                if not dialog_context.stack:
                    # No dialogs to reprompt, just return.
                    return

                await dialog_context.reprompt_dialog()
                return

        # Continue or start the dialog.
        result = await dialog_context.continue_dialog()
        if result.status == DialogTurnStatus.Empty:
            result = await dialog_context.begin_dialog(dialog.id)

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
                    code=EndOfConversationCodes.completed_successfully
                    if result.status == DialogTurnStatus.Complete
                    else EndOfConversationCodes.user_cancelled,
                )
                await turn_context.send_activity(activity)

    @staticmethod
    def __is_from_parent_to_skill(turn_context: TurnContext) -> bool:
        if turn_context.turn_state.get(SkillHandler.SKILL_CONVERSATION_REFERENCE_KEY):
            return False

        claims_identity = turn_context.turn_state.get(BotAdapter.BOT_IDENTITY_KEY)
        return isinstance(
            claims_identity, ClaimsIdentity
        ) and SkillValidation.is_skill_claim(claims_identity.claims)

    @staticmethod
    def __send_eoc_to_parent(turn_context: TurnContext) -> bool:
        claims_identity = turn_context.turn_state.get(BotAdapter.BOT_IDENTITY_KEY)
        if isinstance(
            claims_identity, ClaimsIdentity
        ) and SkillValidation.is_skill_claim(claims_identity.claims):
            # EoC Activities returned by skills are bounced back to the bot by SkillHandler.
            # In those cases we will have a SkillConversationReference instance in state.
            skill_conversation_reference: SkillConversationReference = turn_context.turn_state.get(
                SkillHandler.SKILL_CONVERSATION_REFERENCE_KEY
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
