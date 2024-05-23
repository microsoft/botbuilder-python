# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from copy import deepcopy
from typing import List

from botframework.connector.token_api.models import TokenExchangeRequest
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ExpectedReplies,
    DeliveryModes,
    SignInConstants,
    TokenExchangeInvokeRequest,
)
from botbuilder.core import BotAdapter, TurnContext, ExtendedUserTokenProvider
from botbuilder.core.card_factory import ContentTypes
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
    SKILLCONVERSATIONIDSTATEKEY = (
        "Microsoft.Bot.Builder.Dialogs.SkillDialog.SkillConversationId"
    )

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
        dialog_args = self._validate_begin_dialog_args(options)

        # Create deep clone of the original activity to avoid altering it before forwarding it.
        skill_activity: Activity = deepcopy(dialog_args.activity)

        # Apply conversation reference and common properties from incoming activity before sending.
        TurnContext.apply_conversation_reference(
            skill_activity,
            TurnContext.get_conversation_reference(dialog_context.context.activity),
            is_incoming=True,
        )

        # Store delivery mode in dialog state for later use.
        dialog_context.active_dialog.state[self._deliver_mode_state_key] = (
            dialog_args.activity.delivery_mode
        )

        # Create the conversationId and store it in the dialog context state so we can use it later
        skill_conversation_id = await self._create_skill_conversation_id(
            dialog_context.context, dialog_context.context.activity
        )
        dialog_context.active_dialog.state[SkillDialog.SKILLCONVERSATIONIDSTATEKEY] = (
            skill_conversation_id
        )

        # Send the activity to the skill.
        eoc_activity = await self._send_to_skill(
            dialog_context.context, skill_activity, skill_conversation_id
        )
        if eoc_activity:
            return await dialog_context.end_dialog(eoc_activity.value)

        return self.end_of_turn

    async def continue_dialog(self, dialog_context: DialogContext):
        if not self._on_validate_activity(dialog_context.context.activity):
            return self.end_of_turn

        # Handle EndOfConversation from the skill (this will be sent to the this dialog by the SkillHandler if
        # received from the Skill)
        if dialog_context.context.activity.type == ActivityTypes.end_of_conversation:
            return await dialog_context.end_dialog(
                dialog_context.context.activity.value
            )

        # Create deep clone of the original activity to avoid altering it before forwarding it.
        skill_activity = deepcopy(dialog_context.context.activity)

        skill_activity.delivery_mode = dialog_context.active_dialog.state[
            self._deliver_mode_state_key
        ]

        # Just forward to the remote skill
        skill_conversation_id = dialog_context.active_dialog.state[
            SkillDialog.SKILLCONVERSATIONIDSTATEKEY
        ]
        eoc_activity = await self._send_to_skill(
            dialog_context.context, skill_activity, skill_conversation_id
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

        # connection Name is not applicable for a RePrompt, as we don't expect as OAuthCard in response.
        skill_conversation_id = instance.state[SkillDialog.SKILLCONVERSATIONIDSTATEKEY]
        await self._send_to_skill(context, reprompt_event, skill_conversation_id)

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
            activity = Activity(type=ActivityTypes.end_of_conversation)

            # Apply conversation reference and common properties from incoming activity before sending.
            TurnContext.apply_conversation_reference(
                activity,
                TurnContext.get_conversation_reference(context.activity),
                is_incoming=True,
            )
            activity.channel_data = context.activity.channel_data
            activity.additional_properties = context.activity.additional_properties

            # connection Name is not applicable for an EndDialog, as we don't expect as OAuthCard in response.
            skill_conversation_id = instance.state[
                SkillDialog.SKILLCONVERSATIONIDSTATEKEY
            ]
            await self._send_to_skill(context, activity, skill_conversation_id)

        await super().end_dialog(context, instance, reason)

    def _validate_begin_dialog_args(self, options: object) -> BeginSkillDialogOptions:
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

        return dialog_args

    def _on_validate_activity(
        self, activity: Activity  # pylint: disable=unused-argument
    ) -> bool:
        """
        Validates the activity sent during continue_dialog.

        Override this method to implement a custom validator for the activity being sent during continue_dialog.
        This method can be used to ignore activities of a certain type if needed.
        If this method returns false, the dialog will end the turn without processing the activity.
        """
        return True

    async def _send_to_skill(
        self, context: TurnContext, activity: Activity, skill_conversation_id: str
    ) -> Activity:
        if activity.type == ActivityTypes.invoke:
            # Force ExpectReplies for invoke activities so we can get the replies right away and send
            # them back to the channel if needed. This makes sure that the dialog will receive the Invoke
            # response from the skill and any other activities sent, including EoC.
            activity.delivery_mode = DeliveryModes.expect_replies

        # Always save state before forwarding
        # (the dialog stack won't get updated with the skillDialog and things won't work if you don't)
        await self.dialog_options.conversation_state.save_changes(context, True)

        skill_info = self.dialog_options.skill
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
            # Track sent invoke responses, so more than one is not sent.
            sent_invoke_response = False

            for from_skill_activity in response.body:
                if from_skill_activity.type == ActivityTypes.end_of_conversation:
                    # Capture the EndOfConversation activity if it was sent from skill
                    eoc_activity = from_skill_activity

                    # The conversation has ended, so cleanup the conversation id
                    await self.dialog_options.conversation_id_factory.delete_conversation_reference(
                        skill_conversation_id
                    )
                elif not sent_invoke_response and await self._intercept_oauth_cards(
                    context, from_skill_activity, self.dialog_options.connection_name
                ):
                    # Token exchange succeeded, so no oauthcard needs to be shown to the user
                    sent_invoke_response = True
                else:
                    # If an invoke response has already been sent we should ignore future invoke responses as this
                    # represents a bug in the skill.
                    if from_skill_activity.type == ActivityTypes.invoke_response:
                        if sent_invoke_response:
                            continue
                        sent_invoke_response = True
                    # Send the response back to the channel.
                    await context.send_activity(from_skill_activity)

        return eoc_activity

    async def _create_skill_conversation_id(
        self, context: TurnContext, activity: Activity
    ) -> str:
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
        return skill_conversation_id

    async def _intercept_oauth_cards(
        self, context: TurnContext, activity: Activity, connection_name: str
    ):
        """
        Tells is if we should intercept the OAuthCard message.
        """
        if not connection_name or not isinstance(
            context.adapter, ExtendedUserTokenProvider
        ):
            # The adapter may choose not to support token exchange, in which case we fallback to
            # showing an oauth card to the user.
            return False

        oauth_card_attachment = next(
            attachment
            for attachment in activity.attachments
            if attachment.content_type == ContentTypes.oauth_card
        )
        if oauth_card_attachment:
            oauth_card = oauth_card_attachment.content
            if (
                oauth_card
                and oauth_card.token_exchange_resource
                and oauth_card.token_exchange_resource.uri
            ):
                try:
                    result = await context.adapter.exchange_token(
                        turn_context=context,
                        connection_name=connection_name,
                        user_id=context.activity.from_property.id,
                        exchange_request=TokenExchangeRequest(
                            uri=oauth_card.token_exchange_resource.uri
                        ),
                    )

                    if result and result.token:
                        # If token above is null, then SSO has failed and hence we return false.
                        # If not, send an invoke to the skill with the token.
                        return await self._send_token_exchange_invoke_to_skill(
                            activity,
                            oauth_card.token_exchange_resource.id,
                            oauth_card.connection_name,
                            result.token,
                        )
                except:
                    # Failures in token exchange are not fatal. They simply mean that the user needs
                    # to be shown the OAuth card.
                    return False

        return False

    async def _send_token_exchange_invoke_to_skill(
        self,
        incoming_activity: Activity,
        request_id: str,
        connection_name: str,
        token: str,
    ):
        activity = incoming_activity.create_reply()
        activity.type = ActivityTypes.invoke
        activity.name = SignInConstants.token_exchange_operation_name
        activity.value = TokenExchangeInvokeRequest(
            id=request_id,
            token=token,
            connection_name=connection_name,
        )

        # route the activity to the skill
        skill_info = self.dialog_options.skill
        response = await self.dialog_options.skill_client.post_activity(
            self.dialog_options.bot_id,
            skill_info.app_id,
            skill_info.skill_endpoint,
            self.dialog_options.skill_host_endpoint,
            incoming_activity.conversation.id,
            activity,
        )

        # Check response status: true if success, false if failure
        return response.is_successful_status_code()
