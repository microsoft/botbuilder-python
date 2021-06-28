# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from botbuilder.schema import InvokeResponse

from . import conversation_reference_extension

from .about import __version__
from .activity_handler import ActivityHandler
from .auto_save_state_middleware import AutoSaveStateMiddleware
from .bot import Bot
from .bot_assert import BotAssert
from .bot_adapter import BotAdapter
from .bot_framework_adapter import BotFrameworkAdapter, BotFrameworkAdapterSettings
from .bot_state import BotState
from .bot_state_set import BotStateSet
from .bot_telemetry_client import BotTelemetryClient, Severity
from .card_factory import CardFactory
from .channel_service_handler import BotActionNotImplementedError, ChannelServiceHandler
from .cloud_adapter_base import CloudAdapterBase
from .cloud_channel_service_handler import CloudChannelServiceHandler
from .component_registration import ComponentRegistration
from .conversation_state import ConversationState
from .oauth.extended_user_token_provider import ExtendedUserTokenProvider
from .oauth.user_token_provider import UserTokenProvider
from .intent_score import IntentScore
from .memory_storage import MemoryStorage
from .memory_transcript_store import MemoryTranscriptStore
from .message_factory import MessageFactory
from .middleware_set import AnonymousReceiveMiddleware, Middleware, MiddlewareSet
from .null_telemetry_client import NullTelemetryClient
from .private_conversation_state import PrivateConversationState
from .queue_storage import QueueStorage
from .recognizer import Recognizer
from .recognizer_result import RecognizerResult, TopIntent
from .show_typing_middleware import ShowTypingMiddleware
from .state_property_accessor import StatePropertyAccessor
from .state_property_info import StatePropertyInfo
from .storage import Storage, StoreItem, calculate_change_hash
from .telemetry_constants import TelemetryConstants
from .telemetry_logger_constants import TelemetryLoggerConstants
from .telemetry_logger_middleware import TelemetryLoggerMiddleware
from .turn_context import TurnContext
from .transcript_logger import TranscriptLogger, TranscriptLoggerMiddleware
from .user_state import UserState
from .register_class_middleware import RegisterClassMiddleware
from .adapter_extensions import AdapterExtensions

__all__ = [
    "ActivityHandler",
    "AdapterExtensions",
    "AnonymousReceiveMiddleware",
    "AutoSaveStateMiddleware",
    "Bot",
    "BotActionNotImplementedError",
    "BotAdapter",
    "BotAssert",
    "BotFrameworkAdapter",
    "BotFrameworkAdapterSettings",
    "BotState",
    "BotStateSet",
    "BotTelemetryClient",
    "calculate_change_hash",
    "CardFactory",
    "ChannelServiceHandler",
    "CloudAdapterBase",
    "CloudChannelServiceHandler",
    "ComponentRegistration",
    "ConversationState",
    "conversation_reference_extension",
    "ExtendedUserTokenProvider",
    "IntentScore",
    "InvokeResponse",
    "MemoryStorage",
    "MemoryTranscriptStore",
    "MessageFactory",
    "Middleware",
    "MiddlewareSet",
    "NullTelemetryClient",
    "PrivateConversationState",
    "QueueStorage",
    "RegisterClassMiddleware",
    "Recognizer",
    "RecognizerResult",
    "Severity",
    "ShowTypingMiddleware",
    "StatePropertyAccessor",
    "StatePropertyInfo",
    "Storage",
    "StoreItem",
    "TelemetryConstants",
    "TelemetryLoggerConstants",
    "TelemetryLoggerMiddleware",
    "TopIntent",
    "TranscriptLogger",
    "TranscriptLoggerMiddleware",
    "TurnContext",
    "UserState",
    "UserTokenProvider",
    "__version__",
]
