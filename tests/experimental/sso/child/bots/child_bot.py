from typing import List

from botbuilder.core import (
    ActivityHandler,
    BotFrameworkAdapter,
    ConversationState,
    UserState,
    MessageFactory,
    TurnContext,
)
from botbuilder.dialogs import DialogState
from botframework.connector.auth import MicrosoftAppCredentials

from config import DefaultConfig
from helpers.dialog_helper import DialogHelper
from dialogs import MainDialog


class ChildBot(ActivityHandler):
    def __init__(
        self,
        dialog: MainDialog,
        user_state: UserState,
        conversation_state: ConversationState,
        config: DefaultConfig,
    ):
        self._user_state = user_state
        self._conversation_state = conversation_state
        self._dialog = dialog
        self._connection_name = config.CONNECTION_NAME
        self._config = config

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        await self._conversation_state.save_changes(turn_context)
        await self._user_state.save_changes(turn_context)

    async def on_sign_in_invoke(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        await self._conversation_state.load(turn_context, True)
        await self._user_state.load(turn_context, True)
        await DialogHelper.run_dialog(
            self._dialog,
            turn_context,
            self._conversation_state.create_property(DialogState.__name__)
        )

    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.channel_id != "emulator":
            if "skill login" in turn_context.activity.text:
                await self._conversation_state.load(turn_context, True)
                await self._user_state.load(turn_context, True)
                await DialogHelper.run_dialog(
                    self._dialog,
                    turn_context,
                    self._conversation_state.create_property(DialogState.__name__)
                )
                return
            elif "skill logout" in turn_context.activity.text:
                adapter: BotFrameworkAdapter = turn_context.adapter
                await adapter.sign_out_user(
                    turn_context,
                    self._connection_name,
                    turn_context.activity.from_property.id,
                    MicrosoftAppCredentials(self._config.APP_ID, self._config.APP_PASSWORD))
                await turn_context.send_activity(MessageFactory.text("logout from child bot successful"))
        else:
            await turn_context.send_activity(MessageFactory.text("child: activity (1)"))
            await turn_context.send_activity(MessageFactory.text("child: activity (2)"))
            await turn_context.send_activity(MessageFactory.text("child: activity (3)"))
            await turn_context.send_activity(MessageFactory.text(f"child: {turn_context.activity.text}"))
