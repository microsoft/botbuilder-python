# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .microsoft_app_credentials import MicrosoftAppCredentials
from .government_constants import GovernmentConstants


class MicrosoftGovernmentAppCredentials(MicrosoftAppCredentials):
    """
    MicrosoftGovernmentAppCredentials auth implementation.
    """

    def __init__(
        self,
        app_id: str,
        app_password: str,
        channel_auth_tenant: str = None,
        scope: str = None,
    ):
        super().__init__(
            app_id,
            app_password,
            channel_auth_tenant,
            scope or GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
        )

        # this sets super.oauth_endpoint value
        self.oauth_endpoint = GovernmentConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL

    @staticmethod
    def empty():
        return MicrosoftGovernmentAppCredentials("", "")
