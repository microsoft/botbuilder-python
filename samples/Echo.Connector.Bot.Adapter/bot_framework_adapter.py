# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
from microsoft.botframework.connector import ConnectorClient
from microsoft.botframework.connector.auth import (MicrosoftAppCredentials,
                                                   JwtTokenValidation, SimpleCredentialProvider)
from receive_delegate import ReceiveDelegate

class BotFrameworkAdapter:
    
    def __init__(self, appId, appPassword):
        self._credentials = MicrosoftAppCredentials(appId, appPassword)
        self._credential_provider = SimpleCredentialProvider(appId, appPassword)
        self.on_receive = ReceiveDelegate(None)

    def send(self, activities):
        for activity in activities:
            connector = ConnectorClient(self._credentials, activity.service_url)
            connector.conversations.send_to_conversation(activity.conversation.id, activity)

    def receive(self, authHeader, activity):
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(JwtTokenValidation.assert_valid_activity(
                activity, authHeader, self._credential_provider))
        finally:
            loop.close()
        if hasattr(self, 'on_receive'):
            self.on_receive.call(activity)
