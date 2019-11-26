# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.skills import 

from .config import DefaultConfig

class SkillsConfiguration:
    def __init__(self, configuration: DefaultConfig):
        skills = configuration.BOT_FRAMEWORK_SKILLS
        self.skills = []
        if skills:
            for skill_args in skills:
                self.skills.append()