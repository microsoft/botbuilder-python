# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ConversationState, StatePropertyAccessor
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
        dialog_args = None

    @staticmethod
    def _validate_begin_dialog_options(options: object) -> SkillDialogArgs:
        if not options:
            raise TypeError("options cannot be None.")

        if isinstance(options, dict):
            pass
        elif hasattr(options, ""):
            pass
