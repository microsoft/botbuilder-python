# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict

from botbuilder.schema import ConversationReference


class InspectionSessionsByStatus:
    def __init__(
        self,
        opened_sessions: Dict[str, ConversationReference] = None,
        attached_sessions: Dict[str, ConversationReference] = None,
    ):
        self.opened_sessions: Dict[str, ConversationReference] = opened_sessions or {}
        self.attached_sessions: Dict[str, ConversationReference] = (
            attached_sessions or {}
        )


DEFAULT_INSPECTION_SESSIONS_BY_STATUS = InspectionSessionsByStatus()
