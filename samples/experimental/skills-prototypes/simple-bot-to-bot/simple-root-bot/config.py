# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    SKILL_HOST_ENDPOINT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    BOT_FRAMEWORK_SKILLS = [
        {
            "id": "The bot id for the skill (safest thing is to use your bot handle from the bot registration, "
                  "it should be unique for any bot)",
            "app_id": "The App ID for the skill",
            "skill_endpoint": "The skill URL (i.e.: http://localhost:39783/api/messages)"
        }
    ]
