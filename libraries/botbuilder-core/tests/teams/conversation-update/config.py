#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "5396829c-e0a1-4698-9746-848ca0ba2892")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "x@YOwxU3rqAPzc.nxdRx?Zc.Z96OiHt4")
