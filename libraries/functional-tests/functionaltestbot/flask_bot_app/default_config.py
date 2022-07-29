# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from os import environ


class DefaultConfig:
    """Bot Configuration"""

    PORT: int = 3978
    APP_ID: str = environ.get("MicrosoftAppId", "")
    APP_PASSWORD: str = environ.get("MicrosoftAppPassword", "")
