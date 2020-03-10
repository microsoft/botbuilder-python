# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import json
from typing import List

from jsonpickle import encode
from botbuilder.dialogs import (
    ComponentDialog,
    DialogContext,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.choices import Choice, ListStyle
from botbuilder.dialogs.prompts import PromptOptions, ChoicePrompt
from botbuilder.dialogs.skills import (
    SkillDialogOptions,
    SkillDialog,
    BeginSkillDialogOptions,
)
from botbuilder.core import ConversationState, MessageFactory
from botbuilder.core.skills import BotFrameworkSkill, ConversationIdFactoryBase
from botbuilder.schema import Activity, ActivityTypes, InputHints, DeliveryModes
from botbuilder.integration.aiohttp.skills import SkillHttpClient

from config import SkillConfiguration, DefaultConfig
from .booking_details import BookingDetails
from .tangent_dialog import TangentDialog


class MainDialog(ComponentDialog):

    ACTIVE_SKILL_PROPERTY_NAME = f"MainDialog.ActiveSkillProperty"

    def __init__(
        self,
        conversation_state: ConversationState,
        conversation_id_factory: ConversationIdFactoryBase,
        skill_client: SkillHttpClient,
        skills_config: SkillConfiguration,
        configuration: DefaultConfig,
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self._selected_skill_key = (
            f"{MainDialog.__module__}.{MainDialog.__name__}.SelectedSkillKey"
        )

        bot_id = configuration.APP_ID
        if not bot_id:
            raise TypeError("App Id is not in configuration")

        self._skills_config = skills_config
        if not self._skills_config:
            raise TypeError("Skills configuration cannot be None")

        if not skill_client:
            raise TypeError("skill_client cannot be None")

        if not conversation_state:
            raise TypeError("conversation_state cannot be None")

        # ChoicePrompt to render available skills and skill actions
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))

        # Register the tangent
        self.add_dialog(TangentDialog())

        # Create SkillDialog instances for the configured skills
        for _, skill_info in skills_config.SKILLS.items():
            # SkillDialog used to wrap interaction with the selected skill
            skill_dialog_options = SkillDialogOptions(
                bot_id=bot_id,
                conversation_id_factory=conversation_id_factory,
                skill_client=skill_client,
                skill=skill_info,
                skill_host_endpoint=skills_config.SKILL_HOST_ENDPOINT,
                conversation_state=conversation_state,
            )

            self.add_dialog(SkillDialog(skill_dialog_options, skill_info.id))

        # Main waterfall dialog for this bot
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.select_skill_step,
                    self.select_skill_action_step,
                    self.call_skill_action_step,
                    self.final_step,
                ],
            )
        )

        self._active_skill_property = conversation_state.create_property(
            MainDialog.ACTIVE_SKILL_PROPERTY_NAME
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def on_continue_dialog(self, inner_dc: DialogContext) -> DialogTurnResult:
        # This is an example on how to cancel a SkillDialog that is currently in progress from the parent bot
        active_skill = await self._active_skill_property.get(inner_dc.context)
        activity = inner_dc.context.activity

        if (
            active_skill
            and activity.type == ActivityTypes.message
            and "abort" in activity.text
        ):
            # Cancel all dialog when the user says abort.
            await inner_dc.cancel_all_dialogs()
            return await inner_dc.replace_dialog(self.initial_dialog_id)

        if (
            active_skill
            and activity.type == ActivityTypes.message
            and "tangent" in activity.text
        ):
            # Begin Tangent
            return await inner_dc.replace_dialog(TangentDialog.__name__)

        return await super().on_continue_dialog(inner_dc)

    async def select_skill_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # Create the PromptOptions from the skill configuration which contain the list of configured skills.
        options = PromptOptions(
            prompt=MessageFactory.text("What skill would you like to call?"),
            retry_prompt=MessageFactory.text(
                "That was not a valid choice, please select a valid skill."
            ),
            choices=[
                Choice(value=skill.id)
                for _, skill in self._skills_config.SKILLS.items()
            ],
        )

        # Prompt the user to select a skill.
        return await step_context.prompt(ChoicePrompt.__name__, options)

    async def select_skill_action_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # Get the skill info based on the selected skill.
        selected_skill_id = step_context.result
        selected_skill = self._skills_config.SKILLS.get(selected_skill_id.value)

        # Remember the skill selected by the user.
        step_context.values[self._selected_skill_key] = selected_skill

        # Create the PromptOptions with the actions supported by the selected skill.
        options = PromptOptions(
            prompt=MessageFactory.text(
                f"What action would you like to call in **{selected_skill.id}**?"
            ),
            retry_prompt=MessageFactory.text(
                "That was not a valid choice, please select a valid action."
            ),
            choices=self._get_skill_actions(selected_skill),
            style=ListStyle.suggested_action,
        )

        # Prompt the user to select a skill action.
        return await step_context.prompt(ChoicePrompt.__name__, options)

    async def call_skill_action_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # Starts SkillDialog based on the user's selections
        selected_skill: BotFrameworkSkill = step_context.values[
            self._selected_skill_key
        ]

        if selected_skill.id == "EchoSkillBot":
            # Echo skill only handles message activities, send a dummy utterance to get it started.
            skill_activity = Activity(
                type=ActivityTypes.message,
                attachments=[],
                entities=[],
                text="Start echo skill",
            )
        elif selected_skill.id == "DialogSkillBot":
            skill_activity = self._create_dialog_skill_bot_activity(
                step_context.result.value
            )
        else:
            raise Exception(f"Unknown target skill id: {selected_skill.id}.")

        skill_dialog_args = BeginSkillDialogOptions(skill_activity)

        # We are manually creating the activity to send to the skill, ensure we add the ChannelData and Properties
        # from the original activity so the skill gets them.
        # Note: this is not necessary if we are just forwarding the current activity from context.
        skill_dialog_args.activity.channel_data = (
            step_context.context.activity.channel_data
        )
        skill_dialog_args.activity.additional_properties = (
            step_context.context.activity.additional_properties
        )

        skill_dialog_args.activity.delivery_mode = DeliveryModes.expect_replies

        await self._active_skill_property.set(step_context.context, selected_skill)

        return await step_context.begin_dialog(selected_skill.id, skill_dialog_args)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        active_skill = await self._active_skill_property.get(step_context.context)

        if step_context.result:
            message = "Skill invocation complete."
            message += f" Result: {encode(step_context.result)}"
            await step_context.context.send_activity(
                MessageFactory.text(message, input_hint=InputHints.ignoring_input)
            )

        # Clear the skill selected by the user.
        step_context.values[self._selected_skill_key] = None

        # Clear active skill in state
        await self._active_skill_property.delete(step_context.context)

        # Restart the main dialog with a different message the second time around
        return await step_context.replace_dialog(self.initial_dialog_id)

    # Helper method to create Choice elements for the actions supported by the skill
    def _get_skill_actions(self, skill: BotFrameworkSkill) -> List[Choice]:
        # Note: the bot would probably render this by readying the skill manifest
        # we are just using hardcoded skill actions here for simplicity.

        choices = []
        if skill.id == "EchoSkillBot":
            choices.append(Choice("Messages"))

        elif skill.id == "DialogSkillBot":
            choices.append(Choice("m:some message for tomorrow"))
            choices.append(Choice("BookFlight"))
            choices.append(Choice("OAuthTest"))
            choices.append(Choice("mv:some message with value"))
            choices.append(Choice("BookFlightWithValues"))

        return choices

    # Helper method to create the activity to be sent to the DialogSkillBot
    def _create_dialog_skill_bot_activity(self, selected_option: str) -> Activity:
        # Note: in a real bot, the dialogArgs will be created dynamically based on the conversation
        # and what each action requires, this code hardcodes the values to make things simpler.

        selected_option = selected_option.lower()

        # Send a message activity to the skill.
        if selected_option.startswith("m:"):
            return Activity(
                type=ActivityTypes.message,
                attachments=[],
                entities=[],
                text=selected_option[:2].strip(),
            )

        # Send a message activity to the skill with some artificial parameters in value
        elif selected_option.startswith("mv:"):
            return Activity(
                type=ActivityTypes.message,
                attachments=[],
                entities=[],
                text=selected_option[:3].strip(),
                value=json.dumps(BookingDetails(destination="New York").__dict__),
            )

        # Send an event activity to the skill with "OAuthTest" in the name.
        elif selected_option == "oauthtest":
            return Activity(type=ActivityTypes.event, name="OAuthTest")

        # Send an event activity to the skill with "BookFlight" in the name.
        elif selected_option == "bookflight":
            return Activity(type=ActivityTypes.event, name="BookFlight")

        # Send an event activity to the skill "BookFlight" in the name and some testing values.
        elif selected_option == "bookflightwithvalues":
            return Activity(
                type=ActivityTypes.event,
                name="BookFlight",
                value=json.dumps(BookingDetails(destination="New York", origin="Seattle").__dict__),
            )

        raise Exception(f'Unable to create dialogArgs for "{selected_option}".')
