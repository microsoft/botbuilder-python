# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import Activity
from .bot_framework_skill import BotFrameworkSkill


class SkillConversationIdFactoryOptions:
    def __init__(
        self,
        from_bot_oauth_scope: str,
        from_bot_id: str,
        activity: Activity,
        bot_framework_skill: BotFrameworkSkill,
    ):
        if from_bot_oauth_scope is None:
            raise TypeError(
                "SkillConversationIdFactoryOptions(): from_bot_oauth_scope cannot be None."
            )

        if from_bot_id is None:
            raise TypeError(
                "SkillConversationIdFactoryOptions(): from_bot_id cannot be None."
            )

        if activity is None:
            raise TypeError(
                "SkillConversationIdFactoryOptions(): activity cannot be None."
            )

        if bot_framework_skill is None:
            raise TypeError(
                "SkillConversationIdFactoryOptions(): bot_framework_skill cannot be None."
            )

        self.from_bot_oauth_scope = from_bot_oauth_scope
        self.from_bot_id = from_bot_id
        self.activity = activity
        self.bot_framework_skill = bot_framework_skill
