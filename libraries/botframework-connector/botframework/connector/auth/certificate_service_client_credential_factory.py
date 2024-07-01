# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger

from msrest.authentication import Authentication

from .certificate_app_credentials import CertificateAppCredentials
from .microsoft_app_credentials import MicrosoftAppCredentials
from .service_client_credentials_factory import ServiceClientCredentialsFactory


class CertificateServiceClientCredentialsFactory(ServiceClientCredentialsFactory):
    def __init__(
        self,
        certificate_thumbprint: str,
        certificate_private_key: str,
        app_id: str,
        tenant_id: str = None,
        certificate_public: str = None,
        *,
        logger: Logger = None
    ) -> None:
        """
        CertificateServiceClientCredentialsFactory implementation using a certificate.

        :param certificate_thumbprint:
        :param certificate_private_key:
        :param app_id:
        :param tenant_id:
        :param certificate_public: public_certificate (optional) is public key certificate which will be sent
        through ‘x5c’ JWT header only for subject name and issuer authentication to support cert auto rolls.
        """

        self.certificate_thumbprint = certificate_thumbprint
        self.certificate_private_key = certificate_private_key
        self.app_id = app_id
        self.tenant_id = tenant_id
        self.certificate_public = certificate_public
        self._logger = logger

    async def is_valid_app_id(self, app_id: str) -> bool:
        return app_id == self.app_id

    async def is_authentication_disabled(self) -> bool:
        return not self.app_id

    async def create_credentials(
        self,
        app_id: str,
        oauth_scope: str,
        login_endpoint: str,
        validate_authority: bool,
    ) -> Authentication:
        if await self.is_authentication_disabled():
            return MicrosoftAppCredentials.empty()

        if not await self.is_valid_app_id(app_id):
            raise Exception("Invalid app_id")

        credentials = CertificateAppCredentials(
            app_id,
            self.certificate_thumbprint,
            self.certificate_private_key,
            self.tenant_id,
            oauth_scope,
            self.certificate_public,
        )

        return credentials
