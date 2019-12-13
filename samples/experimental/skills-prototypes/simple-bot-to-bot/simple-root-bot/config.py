#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from typing import Dict
from botbuilder.core.skills import BotFrameworkSkill

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3428
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    SKILL_HOST_ENDPOINT = "http://localhost:3428/api/skills"
    SKILLS = [
        {
            "id": "SkillBot",
            "app_id": "",
            "skill_endpoint": "http://localhost:3978/api/messages",
        },
    ]


class SkillConfiguration:
    SKILL_HOST_ENDPOINT = DefaultConfig.SKILL_HOST_ENDPOINT
    SKILLS: Dict[str, BotFrameworkSkill] = {
        skill["id"]: BotFrameworkSkill(**skill) for skill in DefaultConfig.SKILLS
    }
