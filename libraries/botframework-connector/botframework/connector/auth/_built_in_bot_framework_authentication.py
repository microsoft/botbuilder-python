# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger
from typing import Optional

from botbuilder.schema import Activity

from ..bot_framework_sdk_client_async import BotFrameworkConnectorConfiguration
from ..http_client_factory import HttpClientFactory
from ..skills.bot_framework_client import BotFrameworkClient

from ._bot_framework_client_impl import _BotFrameworkClientImpl
from ._user_token_client_impl import _UserTokenClientImpl
from ._connector_factory_impl import _ConnectorFactoryImpl
from .authenticate_request_result import AuthenticateRequestResult
from .authentication_configuration import AuthenticationConfiguration
from .authentication_constants import AuthenticationConstants
from .bot_framework_authentication import BotFrameworkAuthentication
from .claims_identity import ClaimsIdentity
from .channel_provider import ChannelProvider
from .connector_factory import ConnectorFactory
from .credential_provider import _DelegatingCredentialProvider
from .jwt_token_validation import JwtTokenValidation
from .service_client_credentials_factory import ServiceClientCredentialsFactory
from .skill_validation import SkillValidation
from .simple_channel_provider import SimpleChannelProvider
from .user_token_client import UserTokenClient


class _BuiltinBotFrameworkAuthentication(BotFrameworkAuthentication):
    def __init__(
        self,
        to_channel_from_bot_oauth_scope: str,
        login_endpoint: str,
        caller_id: str,
        channel_service: str,
        oauth_endpoint: str,
        credentials_factory: ServiceClientCredentialsFactory,
        auth_configuration: AuthenticationConfiguration,
        http_client_factory: HttpClientFactory,
        connector_client_configuration: BotFrameworkConnectorConfiguration,
        logger: Logger,
    ):
        self._to_channel_from_bot_oauth_scope = to_channel_from_bot_oauth_scope
        self._login_endpoint = login_endpoint
        self._caller_id = caller_id
        self._channel_service = channel_service
        self._oauth_endpoint = oauth_endpoint
        self._credentials_factory = credentials_factory
        self._auth_configuration = auth_configuration
        self._http_client_factory = http_client_factory
        self._connector_client_configuration = connector_client_configuration
        self._logger = logger

    @staticmethod
    def get_app_id(claims_identity: ClaimsIdentity) -> str:
        # For requests from channel App Id is in Audience claim of JWT token. For emulator it is in AppId claim. For
        # unauthenticated requests we have anonymous claimsIdentity provided auth is disabled.
        # For Activities coming from Emulator AppId claim contains the Bot's AAD AppId.
        app_id = claims_identity.get_claim_value(AuthenticationConstants.AUDIENCE_CLAIM)
        if app_id is None:
            app_id = claims_identity.get_claim_value(
                AuthenticationConstants.APP_ID_CLAIM
            )
        return app_id

    async def authenticate_request(
        self, activity: Activity, auth_header: str
    ) -> AuthenticateRequestResult:
        credential_provider = _DelegatingCredentialProvider(self._credentials_factory)

        claims_identity = await JwtTokenValidation.authenticate_request(
            activity,
            auth_header,
            credential_provider,
            self._get_channel_provider(),
            self._auth_configuration,
        )

        outbound_audience = (
            JwtTokenValidation.get_app_id_from_claims(claims_identity.claims)
            if SkillValidation.is_skill_claim(claims_identity.claims)
            else self._to_channel_from_bot_oauth_scope
        )

        caller_id = await self.generate_caller_id(
            credential_factory=self._credentials_factory,
            claims_identity=claims_identity,
            caller_id=self._caller_id,
        )

        connector_factory = _ConnectorFactoryImpl(
            app_id=_BuiltinBotFrameworkAuthentication.get_app_id(claims_identity),
            to_channel_from_bot_oauth_scope=self._to_channel_from_bot_oauth_scope,
            login_endpoint=self._login_endpoint,
            validate_authority=True,
            credential_factory=self._credentials_factory,
            connector_client_configuration=self._connector_client_configuration,
            logger=self._logger,
        )

        result = AuthenticateRequestResult()
        result.claims_identity = claims_identity
        result.audience = outbound_audience
        result.caller_id = caller_id
        result.connector_factory = connector_factory

        return result

    async def authenticate_streaming_request(
        self, auth_header: str, channel_id_header: str
    ) -> AuthenticateRequestResult:
        credential_provider = _DelegatingCredentialProvider(self._credentials_factory)

        if channel_id_header is None:
            is_auth_disabled = (
                await self._credentials_factory.is_authentication_disabled()
            )
            if not is_auth_disabled:
                raise PermissionError("Unauthorized Access. Request is not authorized")

        claims_identity = await JwtTokenValidation.validate_auth_header(
            auth_header,
            credential_provider,
            self._get_channel_provider(),
            channel_id_header,
        )

        outbound_audience = (
            JwtTokenValidation.get_app_id_from_claims(claims_identity.claims)
            if SkillValidation.is_skill_claim(claims_identity.claims)
            else self._to_channel_from_bot_oauth_scope
        )

        caller_id = await self.generate_caller_id(
            credential_factory=self._credentials_factory,
            claims_identity=claims_identity,
            caller_id=self._caller_id,
        )

        result = AuthenticateRequestResult()
        result.claims_identity = claims_identity
        result.audience = outbound_audience
        result.caller_id = caller_id

        return result

    def create_connector_factory(
        self, claims_identity: ClaimsIdentity
    ) -> ConnectorFactory:
        return _ConnectorFactoryImpl(
            app_id=_BuiltinBotFrameworkAuthentication.get_app_id(claims_identity),
            to_channel_from_bot_oauth_scope=self._to_channel_from_bot_oauth_scope,
            login_endpoint=self._login_endpoint,
            validate_authority=True,
            credential_factory=self._credentials_factory,
            connector_client_configuration=self._connector_client_configuration,
            logger=self._logger,
        )

    async def create_user_token_client(
        self, claims_identity: ClaimsIdentity
    ) -> UserTokenClient:
        app_id = _BuiltinBotFrameworkAuthentication.get_app_id(claims_identity)

        credentials = await self._credentials_factory.create_credentials(
            app_id,
            oauth_scope=self._to_channel_from_bot_oauth_scope,
            login_endpoint=self._login_endpoint,
            validate_authority=True,
        )

        return _UserTokenClientImpl(app_id, credentials, self._oauth_endpoint)

    def create_bot_framework_client(self) -> BotFrameworkClient:
        return _BotFrameworkClientImpl(
            self._credentials_factory,
            self._http_client_factory,
            self._login_endpoint,
            self._logger,
        )

    def get_originating_audience(self) -> str:
        return self._to_channel_from_bot_oauth_scope

    async def authenticate_channel_request(self, auth_header: str) -> ClaimsIdentity:
        credential_provider = _DelegatingCredentialProvider(self._credentials_factory)

        if auth_header is None:
            is_auth_disabled = await credential_provider.is_authentication_disabled()
            if not is_auth_disabled:
                # No auth header. Auth is required. Request is not authorized.
                raise PermissionError("Unauthorized Access. Request is not authorized")

            # In the scenario where auth is disabled, we still want to have the
            # IsAuthenticated flag set in the ClaimsIdentity.
            # To do this requires adding in an empty claim.
            # Since ChannelServiceHandler calls are always a skill callback call, we set the skill claim too.
            return SkillValidation.create_anonymous_skill_claim()

        return await JwtTokenValidation.validate_auth_header(
            auth_header,
            credential_provider,
            channel_service_or_provider=self._get_channel_provider(),
            channel_id="unknown",
            auth_configuration=self._auth_configuration,
        )

    def _get_channel_provider(self) -> Optional[ChannelProvider]:
        return (
            SimpleChannelProvider(self._channel_service)
            if self._channel_service is not None
            else None
        )
