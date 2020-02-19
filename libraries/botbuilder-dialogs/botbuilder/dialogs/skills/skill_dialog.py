# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from copy import deepcopy

from botbuilder.schema import Activity, ActivityTypes
from botbuilder.core import ConversationState, StatePropertyAccessor, TurnContext
from botbuilder.core.skills import BotFrameworkSkill

from botbuilder.dialogs import Dialog, DialogContext

from .skill_dialog_args import SkillDialogArgs
from .skill_dialog_options import SkillDialogOptions


class SkillDialog(Dialog):
    def __init__(
        self, dialog_options: SkillDialogOptions, conversation_state: ConversationState
    ):
        super().__init__(SkillDialog.__name__)
        if not dialog_options:
            raise TypeError("SkillDialog.__init__(): dialog_options cannot be None.")
        if not conversation_state:
            raise TypeError(
                "SkillDialog.__init__(): conversation_state cannot be None."
            )
        self._dialog_options = dialog_options
        self._conversation_state = conversation_state
        self._active_skill_property: StatePropertyAccessor = conversation_state.create_property(
            f"{SkillDialog.__module__}.{SkillDialog.__name__}.ActiveSkillProperty"
        )

    async def begin_dialog(self, dialog_context: DialogContext, options: object = None):
        """
        Method called when a new dialog has been pushed onto the stack and is being activated.
        :param dialog_context: The dialog context for the current turn of conversation.
        :param options: (Optional) additional argument(s) to pass to the dialog being started.
        """
        dialog_args = SkillDialog._validate_begin_dialog_options(options)

        await dialog_context.context.trace_activity(
            f"{SkillDialog.__name__}.BeginDialogAsync()",
            label=f"Using activity of type: {dialog_args.activity.type}",
        )

        # Create deep clone of the original activity to avoid altering it before forwarding it.
        skill_activity: Activity = deepcopy(dialog_args.activity)

        # Apply conversation reference and common properties from incoming activity before sending.
        TurnContext.apply_conversation_reference(
            TurnContext.get_conversation_reference(dialog_context.context.activity),
            True,
        )

        # Send the activity to the skill.
        await self._send_to_skill(dialog_context, skill_activity, dialog_args.Skill)
        return Dialog.end_of_turn

    @staticmethod
    def _validate_begin_dialog_options(options: object) -> SkillDialogArgs:
        if not options:
            raise TypeError("options cannot be None.")

        if isinstance(options, dict) and "skill" in options and "activity" in options:
            skill_args = SkillDialogArgs(
                skill=options["skill"], activity=options["skill"]
            )
        elif hasattr(options, "skill") and hasattr(options, "activity"):
            skill_args = SkillDialogArgs(
                skill=options["skill"], activity=options["skill"]
            )
        else:
            raise TypeError("SkillDialog: options object not valid as SkillDialogArgs.")

        if not skill_args.activity:
            raise TypeError(
                "SkillDialog: activity object in options as SkillDialogArgs cannot be None."
            )

        # Only accept Message or Event activities
        if (
            skill_args.activity.type != ActivityTypes.message
            and skill_args.activity.type != ActivityTypes.event
        ):
            raise TypeError(
                f"Only {ActivityTypes.message} and {ActivityTypes.event} activities are supported."
                f" Received activity of type {skill_args.activity.type}."
            )

        return skill_args

    async def _send_to_skill(
        self,
        dialog_context: DialogContext,
        activity: Activity,
        skill_info: BotFrameworkSkill,
    ):
        # Always save state before forwarding
        # (the dialog stack won't get updated with the skillDialog and things won't work if you don't)
        await self._conversation_state.save_changes(dialog_context.context, True)

        # Create a conversation_id to interact with the skill and send the activity
        skill_conversation_id = await self._dialog_options.conversation_id_factory.create_skill_conversation_id(
            TurnContext.get_conversation_reference(activity)
        )
        response = await self._dialog_options.skill_client.post_activity(
            self._dialog_options.bot_id,
            skill_info.app_id,
            skill_info.skill_endpoint,
            self._dialog_options.skill_host_endpoint,
            skill_conversation_id,
            activity,
        )

        # Inspect the skill response status
        if not (200 <= response.status <= 299):
            raise Exception(
                f'Error invoking the skill id: "{skill_info.id}" at "{skill_info.skill_endpoint}"'
                f" (status is {response.status}). \r\n {response.body}"
            )
