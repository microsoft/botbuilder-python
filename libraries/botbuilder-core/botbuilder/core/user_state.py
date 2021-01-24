# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .turn_context import TurnContext
from .bot_state import BotState
from .storage import Storage


class UserState(BotState):
    """
    Reads and writes user state for your bot to storage.
    """

    no_key_error_message = (
        "UserState: channel_id and/or conversation missing from context.activity."
    )

    def __init__(self, storage: Storage, namespace=""):
        """
        Creates a new UserState instance.
        :param storage:
        :param namespace:
        """
        self.namespace = namespace

        super(UserState, self).__init__(storage, "Internal.UserState")

    def get_storage_key(self, turn_context: TurnContext) -> str:
        """
        Returns the storage key for the current user state.
        :param turn_context:
        :return:
        """
        channel_id = turn_context.activity.channel_id or self.__raise_type_error(
            "invalid activity-missing channelId"
        )
        user_id = turn_context.activity.from_property.id or self.__raise_type_error(
            "invalid activity-missing from_property.id"
        )

        storage_key = None
        if channel_id and user_id:
            storage_key = "%s/users/%s" % (channel_id, user_id)
        return storage_key

    def __raise_type_error(self, err: str = "NoneType found while expecting value"):
        raise TypeError(err)
