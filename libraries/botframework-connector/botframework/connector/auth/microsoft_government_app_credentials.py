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
            scope,
        )

    @staticmethod
    def empty():
        return MicrosoftGovernmentAppCredentials("", "")

    def _get_default_channelauth_tenant(self) -> str:
        return GovernmentConstants.DEFAULT_CHANNEL_AUTH_TENANT

    def _get_to_channel_from_bot_loginurl_prefix(self) -> str:
        return GovernmentConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX

    def _get_to_channel_from_bot_oauthscope(self) -> str:
        return GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
