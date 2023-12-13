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
            channel_auth_tenant or GovernmentConstants.DEFAULT_CHANNEL_AUTH_TENANT,
            scope or GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
        )

    @staticmethod
    def empty():
        return MicrosoftGovernmentAppCredentials("", "")
