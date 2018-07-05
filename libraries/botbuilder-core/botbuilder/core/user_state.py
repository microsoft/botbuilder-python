# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .turn_context import TurnContext
from .bot_state import BotState
from .storage import Storage


class UserState(BotState):
    """
    Reads and writes user state for your bot to storage.
    """

    no_key_error_message = 'UserState: channel_id and/or conversation missing from context.activity.'

    def __init__(self, storage: Storage, namespace=''):
        """
        Creates a new UserState instance.
        :param storage:
        :param namespace:
        """
        self.namespace = namespace

        def call_get_storage_key(context):
            key = self.get_storage_key(context)
            if key is None:
                raise AttributeError(self.no_key_error_message)
            else:
                return key

        super(UserState, self).__init__(storage, call_get_storage_key)

    def get_storage_key(self, context: TurnContext) -> str:
        """
        Returns the storage key for the current user state.
        :param context:
        :return:
        """
        activity = context.activity
        channel_id = getattr(activity, 'channel_id', None)
        user_id = getattr(activity.from_property, 'id', None) if hasattr(activity, 'from_property') else None

        storage_key = None
        if channel_id and user_id:
            storage_key = f"user/{channel_id}/{user_id}/{self.namespace}"
        return storage_key
