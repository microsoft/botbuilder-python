# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
from typing import List
from microsoft.botbuilder.schema import Activity
from microsoft.botframework.connector import ConnectorClient
from microsoft.botframework.connector.auth import (MicrosoftAppCredentials,
                                                   JwtTokenValidation, SimpleCredentialProvider)
from receive_delegate import ReceiveDelegate


class BotFrameworkAdapter:
    
    def __init__(self, app_id: str, app_password: str):
        self._credentials = MicrosoftAppCredentials(app_id, app_password)
        self._credential_provider = SimpleCredentialProvider(app_id, app_password)
        self.on_receive = ReceiveDelegate(None)

    def send(self, activities: List[Activity]):
        for activity in activities:
            connector = ConnectorClient(self._credentials, base_url=activity.service_url)
            connector.conversations.send_to_conversation(activity.conversation.id, activity)

    def receive(self, auth_header: str, activity: Activity):
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(JwtTokenValidation.assert_valid_activity(
                activity, auth_header, self._credential_provider))
        finally:
            loop.close()
        if hasattr(self, 'on_receive'):
            self.on_receive.call(activity)
