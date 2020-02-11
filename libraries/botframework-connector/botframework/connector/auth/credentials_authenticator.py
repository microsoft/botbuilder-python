# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC

from msal import ConfidentialClientApplication

from botframework.connector.auth.authenticator import Authenticator


class CredentialsAuthenticator(Authenticator, ABC):
    def __init__(self, app_id: str, app_password: str, authority: str, scope: str):
        self.app = ConfidentialClientApplication(
            client_id=app_id, client_credential=app_password, authority=authority
        )

        self.scopes = [scope]

    def acquire_token(self):
        # Firstly, looks up a token from cache
        # Since we are looking for token for the current app, NOT for an end user,
        # notice we give account parameter as None.
        auth_token = self.app.acquire_token_silent(self.scopes, account=None)
        if not auth_token:
            # No suitable token exists in cache. Let's get a new one from AAD.
            auth_token = self.app.acquire_token_for_client(scopes=self.scopes)
        return auth_token
