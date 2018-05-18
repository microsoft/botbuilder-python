# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .bot_context import BotContext
from .bot_state import BotState
from .storage import Storage


class UserState(BotState):
    """
    Reads and writes user state for your bot to storage.
    """
    def __init__(self, storage: Storage, namespace=''):
        """
        Creates a new UserState instance.
        :param storage:
        :param namespace:
        """
        self.namespace = namespace
        super(UserState, self).__init__(storage, self.get_storage_key)

    def get_storage_key(self, context: BotContext) -> str:
        """
        Returns the storage key for the current user state.
        :param context:
        :return:
        """
        activity = context.activity
        channel_id = activity.channel_id or None
        user_id = activity.from_property.id or None
        storage_key = None
        if channel_id and user_id:
            storage_key = f"user/{channel_id}/{user_id}/{self.namespace}"
        return storage_key
