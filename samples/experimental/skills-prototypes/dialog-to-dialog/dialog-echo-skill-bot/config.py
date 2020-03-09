#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 39793
    APP_ID = os.environ.get("MicrosoftAppId", "fb7a9f3c-2b30-4ac8-86a0-c44bdeaa380e")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "b0tframew0rks3cr3t!")
