# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from microsoft.botframework.connector import ConnectorClient
from microsoft.botframework.connector.auth import (MicrosoftAppCredentials,
                                                   JwtTokenValidation, SimpleCredentialProvider)

class BotFrameworkAdapter:
    
    def __init__(self, appId, appPassword):
        self._credentials = MicrosoftAppCredentials(appId, appPassword)
        self._credential_provider = SimpleCredentialProvider(appId, appPassword)
        self.on_receive = None

    def send(self, activities):
        for activity in activities:
            connector = ConnectorClient(self._credentials, activity.service_url)
            connector.conversations.send_to_conversation(activity.conversation.id, activity)

    def receive(self, authHeader, activity):
        JwtTokenValidation.assert_valid_activity(activity.service_url, authHeader, self._credential_provider)
        if hasattr(self, 'on_receive'):
            self.on_receive(activity)
