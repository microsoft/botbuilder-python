# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from copy import deepcopy
from typing import List

from botbuilder.schema import Activity, ActivityTypes, ExpectedReplies, DeliveryModes
from botbuilder.core import (
    BotAdapter,
    TurnContext,
)
from botbuilder.core.skills import SkillConversationIdFactoryOptions

from botbuilder.dialogs import (
    Dialog,
    DialogContext,
    DialogEvents,
    DialogReason,
    DialogInstance,
)

from .begin_skill_dialog_options import BeginSkillDialogOptions
from .skill_dialog_options import SkillDialogOptions


class SkillDialog(Dialog):
    def __init__(self, dialog_options: SkillDialogOptions, dialog_id: str):
        super().__init__(dialog_id)
        if not dialog_options:
            raise TypeError("SkillDialog.__init__(): dialog_options cannot be None.")

        self.dialog_options = dialog_options
        self._deliver_mode_state_key = "deliverymode"

    async def begin_dialog(self, dialog_context: DialogContext, options: object = None):
        """
        Method called when a new dialog has been pushed onto the stack and is being activated.
        :param dialog_context: The dialog context for the current turn of conversation.
        :param options: (Optional) additional argument(s) to pass to the dialog being started.
        """
        dialog_args = SkillDialog._validate_begin_dialog_args(options)

        await dialog_context.context.send_trace_activity(
            f"{SkillDialog.__name__}.BeginDialogAsync()",
            label=f"Using activity of type: {dialog_args.activity.type}",
        )

        # Create deep clone of the original activity to avoid altering it before forwarding it.
        skill_activity: Activity = deepcopy(dialog_args.activity)

        # Apply conversation reference and common properties from incoming activity before sending.
        TurnContext.apply_conversation_reference(
            skill_activity,
            TurnContext.get_conversation_reference(dialog_context.context.activity),
            is_incoming=True,
        )

        dialog_context.active_dialog.state[
            self._deliver_mode_state_key
        ] = dialog_args.activity.delivery_mode

        # Send the activity to the skill.
        eoc_activity = await self._send_to_skill(dialog_context.context, skill_activity)
        if eoc_activity:
            return await dialog_context.end_dialog(eoc_activity.value)

        return self.end_of_turn

    async def continue_dialog(self, dialog_context: DialogContext):
        await dialog_context.context.send_trace_activity(
            f"{SkillDialog.__name__}.continue_dialog()",
            label=f"ActivityType: {dialog_context.context.activity.type}",
        )

        # Handle EndOfConversation from the skill (this will be sent to the this dialog by the SkillHandler if
        # received from the Skill)
        if dialog_context.context.activity.type == ActivityTypes.end_of_conversation:
            await dialog_context.context.send_trace_activity(
                f"{SkillDialog.__name__}.continue_dialog()",
                label=f"Got {ActivityTypes.end_of_conversation}",
            )

            return await dialog_context.end_dialog(
                dialog_context.context.activity.value
            )

        # Forward only Message and Event activities to the skill
        if (
            dialog_context.context.activity.type == ActivityTypes.message
            or dialog_context.context.activity.type == ActivityTypes.event
        ):
            # Create deep clone of the original activity to avoid altering it before forwarding it.
            skill_activity = deepcopy(dialog_context.context.activity)
            skill_activity.delivery_mode = dialog_context.active_dialog.state[
                self._deliver_mode_state_key
            ]

            # Just forward to the remote skill
            eoc_activity = await self._send_to_skill(
                dialog_context.context, skill_activity
            )
            if eoc_activity:
                return await dialog_context.end_dialog(eoc_activity.value)

        return self.end_of_turn

    async def reprompt_dialog(  # pylint: disable=unused-argument
        self, context: TurnContext, instance: DialogInstance
    ):
        # Create and send an event to the skill so it can resume the dialog.
        reprompt_event = Activity(
            type=ActivityTypes.event, name=DialogEvents.reprompt_dialog
        )

        # Apply conversation reference and common properties from incoming activity before sending.
        TurnContext.apply_conversation_reference(
            reprompt_event,
            TurnContext.get_conversation_reference(context.activity),
            is_incoming=True,
        )

        await self._send_to_skill(context, reprompt_event)

    async def resume_dialog(  # pylint: disable=unused-argument
        self, dialog_context: "DialogContext", reason: DialogReason, result: object
    ):
        await self.reprompt_dialog(dialog_context.context, dialog_context.active_dialog)
        return self.end_of_turn

    async def end_dialog(
        self, context: TurnContext, instance: DialogInstance, reason: DialogReason
    ):
        # Send of of conversation to the skill if the dialog has been cancelled.
        if reason in (DialogReason.CancelCalled, DialogReason.ReplaceCalled):
            await context.send_trace_activity(
                f"{SkillDialog.__name__}.end_dialog()",
                label=f"ActivityType: {context.activity.type}",
            )
            activity = Activity(type=ActivityTypes.end_of_conversation)

            # Apply conversation reference and common properties from incoming activity before sending.
            TurnContext.apply_conversation_reference(
                activity,
                TurnContext.get_conversation_reference(context.activity),
                is_incoming=True,
            )
            activity.channel_data = context.activity.channel_data
            activity.additional_properties = context.activity.additional_properties

            await self._send_to_skill(context, activity)

        await super().end_dialog(context, instance, reason)

    @staticmethod
    def _validate_begin_dialog_args(options: object) -> BeginSkillDialogOptions:
        if not options:
            raise TypeError("options cannot be None.")

        dialog_args = BeginSkillDialogOptions.from_object(options)

        if not dialog_args:
            raise TypeError(
                "SkillDialog: options object not valid as BeginSkillDialogOptions."
            )

        if not dialog_args.activity:
            raise TypeError(
                "SkillDialog: activity object in options as BeginSkillDialogOptions cannot be None."
            )

        # Only accept Message or Event activities
        if (
            dialog_args.activity.type != ActivityTypes.message
            and dialog_args.activity.type != ActivityTypes.event
        ):
            raise TypeError(
                f"Only {ActivityTypes.message} and {ActivityTypes.event} activities are supported."
                f" Received activity of type {dialog_args.activity.type}."
            )

        return dialog_args

    async def _send_to_skill(
        self, context: TurnContext, activity: Activity,
    ) -> Activity:
        # Create a conversationId to interact with the skill and send the activity
        conversation_id_factory_options = SkillConversationIdFactoryOptions(
            from_bot_oauth_scope=context.turn_state.get(BotAdapter.BOT_OAUTH_SCOPE_KEY),
            from_bot_id=self.dialog_options.bot_id,
            activity=activity,
            bot_framework_skill=self.dialog_options.skill,
        )

        skill_conversation_id = await self.dialog_options.conversation_id_factory.create_skill_conversation_id(
            conversation_id_factory_options
        )

        # Always save state before forwarding
        # (the dialog stack won't get updated with the skillDialog and things won't work if you don't)
        skill_info = self.dialog_options.skill
        await self.dialog_options.conversation_state.save_changes(context, True)

        response = await self.dialog_options.skill_client.post_activity(
            self.dialog_options.bot_id,
            skill_info.app_id,
            skill_info.skill_endpoint,
            self.dialog_options.skill_host_endpoint,
            skill_conversation_id,
            activity,
        )

        # Inspect the skill response status
        if not 200 <= response.status <= 299:
            raise Exception(
                f'Error invoking the skill id: "{skill_info.id}" at "{skill_info.skill_endpoint}"'
                f" (status is {response.status}). \r\n {response.body}"
            )

        eoc_activity: Activity = None
        if activity.delivery_mode == DeliveryModes.expect_replies and response.body:
            # Process replies in the response.Body.
            response.body: List[Activity]
            response.body = ExpectedReplies().deserialize(response.body).activities

            for from_skill_activity in response.body:
                if from_skill_activity.type == ActivityTypes.end_of_conversation:
                    # Capture the EndOfConversation activity if it was sent from skill
                    eoc_activity = from_skill_activity
                else:
                    # Send the response back to the channel.
                    await context.send_activity(from_skill_activity)

        return eoc_activity
