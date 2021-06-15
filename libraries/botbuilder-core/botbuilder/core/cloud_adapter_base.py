# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC

from botframework.connector.auth import BotFrameworkAuthentication
from botframework.connector.skills import bot_framework_client

from .bot_adapter import BotAdapter


class CloudAdapterBase(BotAdapter, ABC):
    def __init__(
        self, bot_framework_authentication: BotFrameworkAuthentication
    ) -> None:
        super().__init__()

        if not bot_framework_authentication:
            raise TypeError("Expected BotFrameworkAuthentication but got None instead")
