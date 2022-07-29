# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger
from typing import Any

from botbuilder.integration.aiohttp import ConfigurationServiceClientCredentialFactory
from botbuilder.schema import Activity
from botframework.connector import HttpClientFactory
from botframework.connector.auth import (
    BotFrameworkAuthentication,
    ClaimsIdentity,
    UserTokenClient,
    ConnectorFactory,
    AuthenticateRequestResult,
    ServiceClientCredentialsFactory,
    AuthenticationConfiguration,
    BotFrameworkAuthenticationFactory,
)
from botframework.connector.skills import BotFrameworkClient


class ConfigurationBotFrameworkAuthentication(BotFrameworkAuthentication):
    def __init__(
        self,
        configuration: Any,
        *,
        credentials_factory: ServiceClientCredentialsFactory = None,
        auth_configuration: AuthenticationConfiguration = None,
        http_client_factory: HttpClientFactory = None,
        logger: Logger = None
    ):
        self._inner: BotFrameworkAuthentication = (
            BotFrameworkAuthenticationFactory.create(
                channel_service=getattr(configuration, "CHANNEL_SERVICE", None),
                validate_authority=getattr(configuration, "VALIDATE_AUTHORITY", True),
                to_channel_from_bot_login_url=getattr(
                    configuration, "TO_CHANNEL_FROM_BOT_LOGIN_URL", None
                ),
                to_channel_from_bot_oauth_scope=getattr(
                    configuration, "TO_CHANNEL_FROM_BOT_OAUTH_SCOPE", None
                ),
                to_bot_from_channel_token_issuer=getattr(
                    configuration, "TO_BOT_FROM_CHANNEL_TOKEN_ISSUER", None
                ),
                oauth_url=getattr(configuration, "OAUTH_URL", None),
                to_bot_from_channel_open_id_metadata_url=getattr(
                    configuration, "TO_BOT_FROM_CHANNEL_OPENID_METADATA_URL", None
                ),
                to_bot_from_emulator_open_id_metadata_url=getattr(
                    configuration, "TO_BOT_FROM_EMULATOR_OPENID_METADATA_URL", None
                ),
                caller_id=getattr(configuration, "CALLER_ID", None),
                credential_factory=(
                    credentials_factory
                    if credentials_factory
                    else ConfigurationServiceClientCredentialFactory(configuration)
                ),
                auth_configuration=(
                    auth_configuration
                    if auth_configuration
                    else AuthenticationConfiguration()
                ),
                http_client_factory=http_client_factory,
                logger=logger,
            )
        )

    async def authenticate_request(
        self, activity: Activity, auth_header: str
    ) -> AuthenticateRequestResult:
        return await self._inner.authenticate_request(activity, auth_header)

    async def authenticate_streaming_request(
        self, auth_header: str, channel_id_header: str
    ) -> AuthenticateRequestResult:
        return await self._inner.authenticate_streaming_request(
            auth_header, channel_id_header
        )

    def create_connector_factory(
        self, claims_identity: ClaimsIdentity
    ) -> ConnectorFactory:
        return self._inner.create_connector_factory(claims_identity)

    async def create_user_token_client(
        self, claims_identity: ClaimsIdentity
    ) -> UserTokenClient:
        return await self._inner.create_user_token_client(claims_identity)

    def create_bot_framework_client(self) -> BotFrameworkClient:
        return self._inner.create_bot_framework_client()

    def get_originating_audience(self) -> str:
        return self._inner.get_originating_audience()

    async def authenticate_channel_request(self, auth_header: str) -> ClaimsIdentity:
        return await self._inner.authenticate_channel_request(auth_header)
