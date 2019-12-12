# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.core import MessageFactory, TurnContext
from botbuilder.schema import ActivityTypes, ChannelAccount

from helpers.dialog_helper import DialogHelper
from bots import DialogBot


class AuthBot(DialogBot):
    async def on_turn(self, turn_context: TurnContext):
        if turn_context.activity.type == ActivityTypes.invoke:
            await DialogHelper.run_dialog(
                self.dialog,
                turn_context,
                self.conversation_state.create_property("DialogState")
            )
        else:
            await super().on_turn(turn_context)

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text("Hello and welcome!")
                )

    async def on_token_response_event(
        self, turn_context: TurnContext
    ):
        print("on token: Running dialog with Message Activity.")

        return await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState")
        )
