#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os


class DefaultConfig:
    """ Bot Configuration """

    PORT = 39793
    APP_ID = os.environ.get("MicrosoftAppId", "fb7a9f3c-2b30-4ac8-86a0-c44bdeaa380e")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "b0tframew0rks3cr3t!")

    # If ALLOWED_CALLERS is empty, any bot can call this Skill.  Add MicrosoftAppIds to restrict
    # callers to only those specified.
    # Example: os.environ.get("AllowedCallers", ["54d3bb6a-3b6d-4ccd-bbfd-cad5c72fb53a"])
    ALLOWED_CALLERS = os.environ.get("AllowedCallers", [])
