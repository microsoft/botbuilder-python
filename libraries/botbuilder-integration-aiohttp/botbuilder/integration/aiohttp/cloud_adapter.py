# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import CloudAdapterBase
from botbuilder.core.streaming import BotFrameworkHttpAdapterBase
from botframework.connector.auth import BotFrameworkAuthentication


class CloudAdapter(CloudAdapterBase, BotFrameworkHttpAdapterBase):
    def __init__(self, bot_framework_authentication: BotFrameworkAuthentication = None):
        super().__init__(bot_framework_authentication)
