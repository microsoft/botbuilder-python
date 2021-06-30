# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger

from msrest.authentication import Authentication

from .authentication_constants import AuthenticationConstants
from .government_constants import GovernmentConstants
from .microsoft_app_credentials import MicrosoftAppCredentials
from .service_client_credentials_factory import ServiceClientCredentialsFactory


class PasswordServiceClientCredentialFactory(ServiceClientCredentialsFactory):
    def __init__(
        self, app_id: str = None, password: str = None, *, logger: Logger = None
    ) -> None:
        self.app_id = app_id
        self.password = password
        self._logger = logger

    async def is_valid_app_id(self, app_id: str) -> bool:
        return app_id == self.app_id

    async def is_authentication_disabled(self) -> bool:
        return not self.app_id

    async def create_credentials(
        self, app_id: str, audience: str, login_endpoint: str, validate_authority: bool
    ) -> Authentication:
        if await self.is_authentication_disabled():
            return MicrosoftAppCredentials.empty()

        if not await self.is_valid_app_id(app_id):
            raise Exception("Invalid app_id")

        credentials: MicrosoftAppCredentials = None
        normalized_endpoint = login_endpoint.lower() if login_endpoint else ""

        if normalized_endpoint.startswith(
            AuthenticationConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX
        ):
            # TODO: Unpack necessity of these empty credentials based on the
            # loginEndpoint as no tokensare fetched when auth is disabled.
            credentials = (
                MicrosoftAppCredentials.empty()
                if not app_id
                else MicrosoftAppCredentials(app_id, self.password, None, audience)
            )
        elif normalized_endpoint == GovernmentConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL:
            credentials = (
                MicrosoftAppCredentials(
                    None,
                    None,
                    None,
                    GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
                )
                if not app_id
                else MicrosoftAppCredentials(app_id, self.password, None, audience)
            )
            normalized_endpoint = login_endpoint
        else:
            credentials = (
                _PrivateCloudAppCredentials(
                    None, None, None, normalized_endpoint, validate_authority
                )
                if not app_id
                else MicrosoftAppCredentials(
                    app_id,
                    self.password,
                    audience,
                    normalized_endpoint,
                    validate_authority,
                )
            )

        return credentials


class _PrivateCloudAppCredentials(MicrosoftAppCredentials):
    def __init__(
        self,
        app_id: str,
        password: str,
        oauth_scope: str,
        oauth_endpoint: str,
        validate_authority: bool,
    ):
        super().__init__(
            app_id, password, channel_auth_tenant=None, oauth_scope=oauth_scope
        )

        self.oauth_endpoint = oauth_endpoint
        self._validate_authority = validate_authority

    @property
    def validate_authority(self):
        return self._validate_authority
