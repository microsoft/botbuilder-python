# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger

from msrest.authentication import Authentication

from .authentication_constants import AuthenticationConstants
from .government_constants import GovernmentConstants
from .microsoft_app_credentials import MicrosoftAppCredentials
from .microsoft_government_app_credentials import MicrosoftGovernmentAppCredentials
from .service_client_credentials_factory import ServiceClientCredentialsFactory


class PasswordServiceClientCredentialFactory(ServiceClientCredentialsFactory):
    def __init__(
        self,
        app_id: str = None,
        password: str = None,
        tenant_id: str = None,
        *,
        logger: Logger = None
    ) -> None:
        self.app_id = app_id
        self.password = password
        self.tenant_id = tenant_id
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

        credentials: MicrosoftAppCredentials
        normalized_endpoint = login_endpoint.lower() if login_endpoint else ""

        if normalized_endpoint.startswith(
            AuthenticationConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX
        ):
            credentials = MicrosoftAppCredentials(
                app_id, self.password, self.tenant_id, oauth_scope
            )
        elif normalized_endpoint.startswith(
            GovernmentConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX
        ):
            credentials = MicrosoftGovernmentAppCredentials(
                app_id,
                self.password,
                self.tenant_id,
                oauth_scope,
            )
        else:
            credentials = _PrivateCloudAppCredentials(
                app_id,
                self.password,
                self.tenant_id,
                oauth_scope,
                login_endpoint,
                validate_authority,
            )

        return credentials


class _PrivateCloudAppCredentials(MicrosoftAppCredentials):
    def __init__(
        self,
        app_id: str,
        password: str,
        tenant_id: str,
        oauth_scope: str,
        oauth_endpoint: str,
        validate_authority: bool,
    ):
        super().__init__(
            app_id, password, channel_auth_tenant=tenant_id, oauth_scope=oauth_scope
        )

        self.oauth_endpoint = oauth_endpoint
        self._validate_authority = validate_authority

    @property
    def validate_authority(self):
        return self._validate_authority
