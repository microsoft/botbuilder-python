# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger

from msrest.authentication import Authentication

from .authentication_constants import AuthenticationConstants
from .government_constants import GovernmentConstants
from .certificate_app_credentials import CertificateAppCredentials
from .certificate_government_app_credentials import CertificateGovernmentAppCredentials
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

        normalized_endpoint = login_endpoint.lower() if login_endpoint else ""

        if normalized_endpoint.startswith(
            AuthenticationConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX
        ):
            credentials = CertificateAppCredentials(
                app_id,
                self.certificate_thumbprint,
                self.certificate_private_key,
                self.tenant_id,
                oauth_scope,
                self.certificate_public,
            )
        elif normalized_endpoint.startswith(
            GovernmentConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX
        ):
            credentials = CertificateGovernmentAppCredentials(
                app_id,
                self.certificate_thumbprint,
                self.certificate_private_key,
                self.tenant_id,
                oauth_scope,
                self.certificate_public,
            )
        else:
            credentials = _CertificatePrivateCloudAppCredentials(
                app_id,
                self.certificate_thumbprint,
                self.certificate_private_key,
                self.tenant_id,
                oauth_scope,
                self.certificate_public,
                login_endpoint,
                validate_authority,
            )

        return credentials


class _CertificatePrivateCloudAppCredentials(CertificateAppCredentials):
    def __init__(
        self,
        app_id: str,
        certificate_thumbprint: str,
        certificate_private_key: str,
        channel_auth_tenant: str,
        oauth_scope: str,
        certificate_public: str,
        oauth_endpoint: str,
        validate_authority: bool,
    ):
        super().__init__(
            app_id,
            certificate_thumbprint,
            certificate_private_key,
            channel_auth_tenant,
            oauth_scope,
            certificate_public,
        )

        self.oauth_endpoint = oauth_endpoint
        self._validate_authority = validate_authority

    @property
    def validate_authority(self):
        return self._validate_authority
