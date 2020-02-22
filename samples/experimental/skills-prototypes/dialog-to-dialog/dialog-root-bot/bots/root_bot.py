import json
import os.path

from typing import List

from botbuilder.core import (
    ActivityHandler,
    BotFrameworkHttpClient,
    ConversationState,
    MessageFactory,
    TurnContext,
)
from botbuilder.core.skills import SkillConversationIdFactory
from botbuilder.dialogs import Dialog

from botbuilder.schema import ActivityTypes, Attachment, ChannelAccount

from config import DefaultConfig, SkillConfiguration
from helpers.dialog_helper import DialogHelper


class RootBot(ActivityHandler):
    def __init__(
        self, conversation_state: ConversationState, main_dialog: Dialog,
    ):
        self._conversation_state = conversation_state
        self._main_dialog = main_dialog

    async def on_turn(self, turn_context: TurnContext):
        if turn_context.activity.type == ActivityTypes.conversation_update:
            # Handle end of conversation back from the skill
            # forget skill invocation
            await DialogHelper.run_dialog(
                self._main_dialog,
                turn_context,
                self._conversation_state.create_property("DialogState"),
            )
        else:
            await super().on_turn(turn_context)

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                welcome_card = self._create_adaptive_card_attachment()
                activity = MessageFactory.attachment(welcome_card)
                await turn_context.send_activity(activity)
                await DialogHelper.run_dialog(
                    self._main_dialog,
                    turn_context,
                    self._conversation_state.create_property("DialogState"),
                )

    def _create_adaptive_card_attachment(self) -> Attachment:
        relative_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(relative_path, "../cards/welcomeCard.json")
        with open(path) as in_file:
            card = json.load(in_file)

        return Attachment(
            content_type="application/vnd.microsoft.card.adaptive", content=card
        )
