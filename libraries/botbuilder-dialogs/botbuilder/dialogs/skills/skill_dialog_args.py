# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import Activity
from botbuilder.core.skills import BotFrameworkSkill


class SkillDialogArgs:
    def __init__(self, skill: BotFrameworkSkill = None, activity: Activity = None):
        self.skill = skill
        self.activity = activity
