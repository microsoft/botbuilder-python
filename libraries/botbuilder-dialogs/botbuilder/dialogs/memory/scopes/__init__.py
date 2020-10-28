# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from .bot_state_memory_scope import BotStateMemoryScope
from .class_memory_scope import ClassMemoryScope
from .conversation_memory_scope import ConversationMemoryScope
from .dialog_class_memory_scope import DialogClassMemoryScope
from .dialog_context_memory_scope import DialogContextMemoryScope
from .dialog_memory_scope import DialogMemoryScope
from .memory_scope import MemoryScope
from .settings_memory_scope import SettingsMemoryScope
from .this_memory_scope import ThisMemoryScope
from .turn_memory_scope import TurnMemoryScope
from .user_memory_scope import UserMemoryScope


__all__ = [
    "BotStateMemoryScope",
    "ClassMemoryScope",
    "ConversationMemoryScope",
    "DialogClassMemoryScope",
    "DialogContextMemoryScope",
    "DialogMemoryScope",
    "MemoryScope",
    "SettingsMemoryScope",
    "ThisMemoryScope",
    "TurnMemoryScope",
    "UserMemoryScope",
]
