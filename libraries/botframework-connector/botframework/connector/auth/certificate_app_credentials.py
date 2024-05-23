# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC

from msal import ConfidentialClientApplication

from .app_credentials import AppCredentials


class CertificateAppCredentials(AppCredentials, ABC):
    """
    AppCredentials implementation using a certificate.

    See:
    https://github.com/AzureAD/microsoft-authentication-library-for-python/wiki/Client-Credentials#client-credentials-with-certificate
    """

    def __init__(
        self,
        app_id: str,
        certificate_thumbprint: str,
        certificate_private_key: str,
        channel_auth_tenant: str = None,
        oauth_scope: str = None,
        certificate_public: str = None,
    ):
        """
        AppCredentials implementation using a certificate.

        :param app_id:
        :param certificate_thumbprint:
        :param certificate_private_key:
        :param channel_auth_tenant:
        :param oauth_scope:
        :param certificate_public: public_certificate (optional) is public key certificate which will be sent
        through ‘x5c’ JWT header only for subject name and issuer authentication to support cert auto rolls.
        """

        # super will set proper scope and endpoint.
        super().__init__(
            app_id=app_id,
            channel_auth_tenant=channel_auth_tenant,
            oauth_scope=oauth_scope,
        )

        self.scopes = [self.oauth_scope]
        self.app = None
        self.certificate_thumbprint = certificate_thumbprint
        self.certificate_private_key = certificate_private_key
        self.certificate_public = certificate_public

    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        Implementation of AppCredentials.get_token.
        :return: The access token for the given certificate.
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
                authority=self.oauth_endpoint,
                client_credential={
                    "thumbprint": self.certificate_thumbprint,
                    "private_key": self.certificate_private_key,
                    "public_certificate": (
                        self.certificate_public if self.certificate_public else None
                    ),
                },
            )

        return self.app
