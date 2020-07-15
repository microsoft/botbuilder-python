# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from warnings import warn

from botbuilder.core import (
    BotAdapter,
    BotState,
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
    def use_bot_state(
        bot_adapter: BotAdapter, *bot_states: BotState, auto: bool = True
    ) -> BotAdapter:
        """
        Registers bot state object into the TurnContext. The botstate will be available via the turn context.

        :param bot_adapter: The BotAdapter on which to register the state objects.
        :param bot_states: One or more BotState objects to register.
        :return: The updated adapter.
        """
        if not bot_states:
            raise TypeError("At least one BotAdapter is required")

        for bot_state in bot_states:
            bot_adapter.use(
                RegisterClassMiddleware(
                    bot_state, AdapterExtensions.fullname(bot_state)
                )
            )

        if auto:
            bot_adapter.use(AutoSaveStateMiddleware(bot_states))

        return bot_adapter

    @staticmethod
    def fullname(obj):
        module = obj.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return obj.__class__.__name__  # Avoid reporting __builtin__
        return module + "." + obj.__class__.__name__

    @staticmethod
    def use_state(
        adapter: BotAdapter,
        user_state: UserState,
        conversation_state: ConversationState,
        auto: bool = True,
    ) -> BotAdapter:
        """
        [DEPRECATED] Registers user and conversation state objects with the adapter. These objects will be available via
        the turn context's `turn_state` property.

        :param adapter: The BotAdapter on which to register the state objects.
        :param user_state: The UserState object to register.
        :param conversation_state: The ConversationState object to register.
        :param auto: True to automatically persist state each turn.
        :return: The BotAdapter
        """
        warn(
            "This method is deprecated in 4.9. You should use the method .use_bot_state() instead.",
            DeprecationWarning,
        )

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
