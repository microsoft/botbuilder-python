# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .bot_state import BotState
from .turn_context import TurnContext
from .storage import Storage


class PrivateConversationState(BotState):
    def __init__(self, storage: Storage, namespace: str = ""):
        async def aux_func(context: TurnContext) -> str:
            nonlocal self
            return await self.get_storage_key(context)

        self.namespace = namespace
        super().__init__(storage, aux_func)

    def get_storage_key(self, turn_context: TurnContext) -> str:
        activity = turn_context.activity
        channel_id = activity.channel_id if activity is not None else None

        if not channel_id:
            raise Exception("missing activity.channel_id")

        if activity and activity.conversation and activity.conversation.id is not None:
            conversation_id = activity.conversation.id
        else:
            raise Exception("missing activity.conversation.id")

        if (
            activity
            and activity.from_property
            and activity.from_property.id is not None
        ):
            user_id = activity.from_property.id
        else:
            raise Exception("missing activity.from_property.id")

        return f"{channel_id}/conversations/{ conversation_id }/users/{ user_id }/{ self.namespace }"
