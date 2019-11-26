#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "e4c570ca-189d-4fee-a81b-5466be24a557")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "bghqYKJV3709;creKFP8$@@")
