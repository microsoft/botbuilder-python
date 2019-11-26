# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, ConversationState

from ..skills

class RootBot(ActivityHandler):
    def __init__(self, conversation_state: ConversationState, skills_config)