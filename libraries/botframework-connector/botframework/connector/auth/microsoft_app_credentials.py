# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC

from .app_credentials import AppCredentials
from .authenticator import Authenticator
from .credentials_authenticator import CredentialsAuthenticator


class MicrosoftAppCredentials(AppCredentials, ABC):
    """
    MicrosoftAppCredentials auth implementation.
    """

    MICROSOFT_APP_ID = "MicrosoftAppId"
    MICROSOFT_PASSWORD = "MicrosoftPassword"

    def __init__(
        self,
        app_id: str,
        password: str,
        channel_auth_tenant: str = None,
        oauth_scope: str = None,
    ):
        super().__init__(
            channel_auth_tenant=channel_auth_tenant, oauth_scope=oauth_scope
        )
        self.microsoft_app_id = app_id
        self.microsoft_app_password = password

    def _build_authenticator(self) -> Authenticator:
        """
        Returns an Authenticator suitable for credential auth.
        :return: An Authenticator object
        """
        return CredentialsAuthenticator(
            app_id=self.microsoft_app_id,
            app_password=self.microsoft_app_password,
            authority=self.oauth_endpoint,
            scope=self.oauth_scope,
        )
