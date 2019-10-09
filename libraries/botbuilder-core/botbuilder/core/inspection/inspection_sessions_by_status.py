# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict

from msrest.serialization import Model

from botbuilder.core import BotState
from botbuilder.schema import ChannelAccount, ConversationAccount, ConversationReference


class InspectionSessionsByStatus(Model):
    _attribute_map = {
        "opened_sessions": {"key": "openedSessions", "type": "{ConversationReference}"},
        "attached_sessions": {
            "key": "attachedSessions",
            "type": "{ConversationReference}",
        },
    }

    def __init__(
        self,
        opened_sessions: Dict[str, ConversationReference] = None,
        attached_sessions: Dict[str, ConversationReference] = None,
        **kwargs
    ):
        super(InspectionSessionsByStatus, self).__init__(**kwargs)
        self.opened_sessions: Dict[str, ConversationReference] = opened_sessions or {}
        self.attached_sessions: Dict[
            str, ConversationReference
        ] = attached_sessions or {}


DEFAULT_INSPECTION_SESSIONS_BY_STATUS = InspectionSessionsByStatus()

BotState.register_msrest_deserializer(
    InspectionSessionsByStatus,
    dependencies=[ChannelAccount, ConversationAccount, ConversationReference],
)
