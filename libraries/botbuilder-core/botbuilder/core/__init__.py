# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from .about import __version__

from .bot_adapter import BotAdapter
from .bot_framework_adapter import BotFrameworkAdapter, BotFrameworkAdapterSettings
from .bot_context import BotContext
from .bot_state import BotState
from .card_factory import CardFactory
from .conversation_state import ConversationState
from .memory_storage import MemoryStorage
from .message_factory import MessageFactory
from .middleware_set import AnonymousReceiveMiddleware, Middleware, MiddlewareSet
from .storage import Storage, StoreItem, StorageKeyFactory, calculate_change_hash
from .test_adapter import TestAdapter
from .user_state import UserState

"""Expose botbuilder-schema in botbuilder-core."""
from botbuilder.schema import *
import botbuilder.schema

__all__ = [class_name for class_name in dir(botbuilder.schema) if class_name[0].isupper()]

"""Add to __all__ the classes from botbuilder-core."""
__all__.extend(['AnonymousReceiveMiddleware',
                'BotAdapter',
                'BotContext',
                'BotFrameworkAdapter',
                'BotFrameworkAdapterSettings',
                'BotState',
                'calculate_change_hash',
                'CardFactory',
                'ConversationState',
                'MemoryStorage',
                'MessageFactory',
                'Middleware',
                'MiddlewareSet',
                'Storage',
                'StorageKeyFactory',
                'StoreItem',
                'TestAdapter',
                'UserState',
                '__version__'])
