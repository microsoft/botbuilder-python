# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from botbuilder.core import (
    BotAdapter,
    Storage,
    RegisterClassMiddleware,
    UserState,
    ConversationState,
    AutoSaveStateMiddleware,
)


class AdapterExtensions:
    @staticmethod
    def use_storage(adapter: BotAdapter, storage: Storage) -> BotAdapter:
        """
        Registers a storage layer with the adapter. The storage object will be available via the turn context's
        `turn_state` property.

        :param adapter: The BotAdapter on which to register the storage object.
        :param storage: The Storage object to register.
        :return: The BotAdapter
        """
        return adapter.use(RegisterClassMiddleware(storage))

    @staticmethod
    def use_state(
        adapter: BotAdapter,
        user_state: UserState,
        conversation_state: ConversationState,
        auto: bool = True,
    ) -> BotAdapter:
        """
        Registers user and conversation state objects with the adapter. These objects will be available via
        the turn context's `turn_state` property.

        :param adapter: The BotAdapter on which to register the state objects.
        :param user_state: The UserState object to register.
        :param conversation_state: The ConversationState object to register.
        :param auto: True to automatically persist state each turn.
        :return: The BotAdapter
        """
        if not adapter:
            raise TypeError("BotAdapter is required")

        if not user_state:
            raise TypeError("UserState is required")

        if not conversation_state:
            raise TypeError("ConversationState is required")

        adapter.use(RegisterClassMiddleware(user_state))
        adapter.use(RegisterClassMiddleware(conversation_state))

        if auto:
            adapter.use(AutoSaveStateMiddleware([user_state, conversation_state]))

        return adapter
