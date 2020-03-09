#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from typing import Dict
from botbuilder.core.skills import BotFrameworkSkill


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "b56a1b59-7081-4546-b3fa-177401fd0657")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "b0tframew0rks3cr3t!")
    SKILL_HOST_ENDPOINT = "http://localhost:3978/api/skills"
    SKILLS = [
        {
            "id": "EchoSkillBot",
            "app_id": "fb7a9f3c-2b30-4ac8-86a0-c44bdeaa380e",
            "skill_endpoint": "http://localhost:39793/api/messages",
        },
        {
            "id": "DialogSkillBot",
            "app_id": "67ec4e96-f4f6-424b-911f-de362a2a81d4",
            "skill_endpoint": "http://localhost:39783/api/messages",
        },
    ]


class SkillConfiguration:
    SKILL_HOST_ENDPOINT = DefaultConfig.SKILL_HOST_ENDPOINT
    SKILLS: Dict[str, BotFrameworkSkill] = {
        skill["id"]: BotFrameworkSkill(**skill) for skill in DefaultConfig.SKILLS
    }
