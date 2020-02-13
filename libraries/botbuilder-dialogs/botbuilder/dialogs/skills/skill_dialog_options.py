# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core.skills import BotFrameworkClient, SkillConversationIdFactory


class SkillDialogOptions:
    def __init__(
        self,
        bot_id: str = None,
        skill_client: BotFrameworkClient = None,
        skill_host_endpoint: str = None,
        conversation_id_factory: SkillConversationIdFactory = None,
    ):
        self.bot_id = bot_id
        self.skill_client = skill_client
        self.skill_host_endpoint = skill_host_endpoint
        self.conversation_id_factory = conversation_id_factory
