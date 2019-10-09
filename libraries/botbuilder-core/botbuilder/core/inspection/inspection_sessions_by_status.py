# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict

from botbuilder.schema import ConversationReference


class InspectionSessionsByStatus:
    def __init__(self):
        self.opened_sessions: Dict[str, ConversationReference] = {}
        self.attached_sessions: Dict[str, ConversationReference] = {}


DEFAULT_INSPECTION_SESSIONS_BY_STATUS = InspectionSessionsByStatus()
