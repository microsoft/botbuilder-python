# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botframework.connector.auth import MicrosoftAppCredentials, GovernmentConstants


class MicrosoftGovernmentAppCredentials(MicrosoftAppCredentials):
    """
    MicrosoftGovernmentAppCredentials auth implementation.
    """

    def __init__(
        self,
        app_id: str,
        app_password: str,
        channel_auth_tenant: str = None,
        scope: str = GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
    ):
        super().__init__(app_id, app_password, channel_auth_tenant, scope)
        self.oauth_endpoint = GovernmentConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL

    @staticmethod
    def empty():
        return MicrosoftGovernmentAppCredentials("", "")
