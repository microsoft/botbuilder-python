# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger

from msrest.authentication import Authentication

from .managedidentity_app_credentials import ManagedIdentityAppCredentials
from .microsoft_app_credentials import MicrosoftAppCredentials
from .service_client_credentials_factory import ServiceClientCredentialsFactory


class ManagedIdentityServiceClientCredentialsFactory(ServiceClientCredentialsFactory):
    def __init__(self, app_id: str = None, *, logger: Logger = None) -> None:
        self.app_id = app_id
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

        credentials = ManagedIdentityAppCredentials(app_id, oauth_scope)

        return credentials
