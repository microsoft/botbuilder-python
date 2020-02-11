# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC

from msal import ConfidentialClientApplication

from botframework.connector.auth.authenticator import Authenticator


class CertificateAuthenticator(Authenticator, ABC):
    """
    Retrieves a token using a certificate.

    This class is using MSAL for AAD authentication.

    For certificate creation and setup see:
    https://github.com/AzureAD/microsoft-authentication-library-for-python/wiki/Client-Credentials#client-credentials-with-certificate
    """

    def __init__(
        self,
        app_id: str,
        certificate_thumbprint: str,
        certificate_private_key: str,
        authority: str,
        scope: str,
    ):
        self.app = ConfidentialClientApplication(
            client_id=app_id,
            authority=authority,
            client_credential={
                "thumbprint": certificate_thumbprint,
                "private_key": certificate_private_key,
            },
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
