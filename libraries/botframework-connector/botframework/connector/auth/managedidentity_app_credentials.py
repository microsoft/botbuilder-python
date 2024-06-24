# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC

import msal
import requests

from .app_credentials import AppCredentials
from .microsoft_app_credentials import MicrosoftAppCredentials


class ManagedIdentityAppCredentials(AppCredentials, ABC):
    """
    AppCredentials implementation using application ID and password.
    """

    global_token_cache = msal.TokenCache()

    def __init__(self, app_id: str, oauth_scope: str = None):
        # super will set proper scope and endpoint.
        super().__init__(
            app_id=app_id,
            oauth_scope=oauth_scope,
        )

        self._managed_identity = {"ManagedIdentityIdType": "ClientId", "Id": app_id}

        self.app = None

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
        auth_token = self.__get_msal_app().acquire_token_for_client(
            resource=self.oauth_scope
        )
        return auth_token["access_token"]

    def __get_msal_app(self):
        if not self.app:
            self.app = msal.ManagedIdentityClient(
                self._managed_identity,
                http_client=requests.Session(),
                token_cache=ManagedIdentityAppCredentials.global_token_cache,
            )
        return self.app
