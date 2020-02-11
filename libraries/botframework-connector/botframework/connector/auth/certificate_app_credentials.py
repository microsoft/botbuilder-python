# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC

from .app_credentials import AppCredentials
from .authenticator import Authenticator
from .certificate_authenticator import CertificateAuthenticator


class CertificateAppCredentials(AppCredentials, ABC):
    """
    CertificateAppCredentials auth implementation.
    """

    def __init__(
        self,
        app_id: str,
        certificate_thumbprint: str,
        certificate_private_key: str,
        channel_auth_tenant: str = None,
        oauth_scope: str = None,
    ):
        super().__init__(
            channel_auth_tenant=channel_auth_tenant, oauth_scope=oauth_scope
        )
        self.microsoft_app_id = app_id
        self.certificate_thumbprint = certificate_thumbprint
        self.certificate_private_key = certificate_private_key

    def _build_authenticator(self) -> Authenticator:
        """
        Returns an Authenticator suitable for certificate auth.
        :return: An Authenticator object
        """
        return CertificateAuthenticator(
            app_id=self.microsoft_app_id,
            certificate_thumbprint=self.certificate_thumbprint,
            certificate_private_key=self.certificate_private_key,
            authority=self.oauth_endpoint,
            scope=self.oauth_scope,
        )
