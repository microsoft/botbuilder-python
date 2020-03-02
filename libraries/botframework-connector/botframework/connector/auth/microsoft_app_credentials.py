# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC

import requests
from msal import ConfidentialClientApplication

from .app_credentials import AppCredentials


class MicrosoftAppCredentials(AppCredentials, ABC):
    """
    AppCredentials implementation using application ID and password.
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
        # super will set proper scope and endpoint.
        super().__init__(
            app_id=app_id,
            channel_auth_tenant=channel_auth_tenant,
            oauth_scope=oauth_scope,
        )

        self.microsoft_app_password = password
        self.app = None

        # This check likely needs to be more nuanced than this.  Assuming
        # "/.default" precludes other valid suffixes
        scope = self.oauth_scope
        if oauth_scope and not scope.endswith("/.default"):
            scope += "/.default"
        self.scopes = [scope]

    @staticmethod
    def empty():
        return MicrosoftAppCredentials("", "")

    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        Implementation of AppCredentials.get_token.
        :return: The access token for the given app id and password.
        """

        # Firstly, looks up a token from cache
        # Since we are looking for token for the current app, NOT for an end user,
        # notice we give account parameter as None.
        auth_token = self.__get_msal_app().acquire_token_silent(
            self.scopes, account=None
        )
        if not auth_token:
            # No suitable token exists in cache. Let's get a new one from AAD.
            auth_token = self.__get_msal_app().acquire_token_for_client(
                scopes=self.scopes
            )
        return auth_token["access_token"]

    def __get_msal_app(self):
        if not self.app:
            self.app = ConfidentialClientApplication(
                client_id=self.microsoft_app_id,
                client_credential=self.microsoft_app_password,
                authority=self.oauth_endpoint,
            )

        return self.app

    def _should_authorize(self, session: requests.Session) -> bool:
        """
        Override of AppCredentials._should_authorize
        :param session:
        :return:
        """
        return self.microsoft_app_id and self.microsoft_app_password
