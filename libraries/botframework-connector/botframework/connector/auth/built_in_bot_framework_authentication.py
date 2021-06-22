from logging import Logger
from typing import Optional

from botbuilder.schema import Activity
from botframework.connector.auth import (
    BotFrameworkAuthentication,
    AuthenticateRequestResult,
    ClaimsIdentity,
    UserTokenClient,
    ConnectorFactory,
    ServiceClientCredentialsFactory,
    AuthenticationConfiguration,
    AuthenticationConstants,
    SkillValidation,
    JwtTokenValidation,
    ChannelProvider,
    SimpleChannelProvider
)
from botframework.connector import HttpClientFactory
from botframework.connector.auth.connector_factory import _ConnectorFactoryImpl
from botframework.connector.auth.credential_provider import _DelegatingCredentialProvider
from botframework.connector.skills import BotFrameworkClient


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
        logger: Logger
    ):
        self._to_channel_from_bot_oauth_scope = to_channel_from_bot_oauth_scope
        self._login_endpoint = login_endpoint
        self._caller_id = caller_id
        self._channel_service = channel_service
        self._oauth_endpoint = oauth_endpoint
        self._credentials_factory = credentials_factory
        self._auth_configuration = auth_configuration
        self._http_client_factory = http_client_factory
        self._logger = logger

    @staticmethod
    def get_app_id(claims_identity: ClaimsIdentity) -> str:
        # For requests from channel App Id is in Audience claim of JWT token. For emulator it is in AppId claim. For
        # unauthenticated requests we have anonymous claimsIdentity provided auth is disabled.
        # For Activities coming from Emulator AppId claim contains the Bot's AAD AppId.
        app_id = claims_identity.get_claim_value(AuthenticationConstants.AUDIENCE_CLAIM)
        if app_id is None:
            app_id = claims_identity.get_claim_value(AuthenticationConstants.APP_ID_CLAIM)
        return app_id

    async def authenticate_request(
        self, activity: Activity, auth_header: str
    ) -> AuthenticateRequestResult:
        credential_provider = _DelegatingCredentialProvider(self._credentials_factory)

        claims_identity = await JwtTokenValidation.authenticate_request(
            activity, auth_header, credential_provider, self._get_channel_provider(), self._auth_configuration
        )

        outbound_audience = (
            JwtTokenValidation.get_app_id_from_claims(claims_identity.claims)
            if SkillValidation.is_skill_claim(claims_identity.claims) else
            self._to_channel_from_bot_oauth_scope
        )

        caller_id = await self.generate_caller_id(
            self._credentials_factory, claims_identity, self._caller_id
        )

        connector_factory = _ConnectorFactoryImpl(
            app_id=_BuiltinBotFrameworkAuthentication.get_app_id(claims_identity),
            to_channel_from_bot_oauth_scope=self._to_channel_from_bot_oauth_scope,
            login_endpoint=self._login_endpoint,
            validate_authority=True,
            credentials_factory=self._credentials_factory,
            http_client_factory=self._http_client_factory,
            logger=self._logger
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
            is_auth_disabled = await self._credentials_factory.is_authentication_disabled()
            if not is_auth_disabled:
                raise PermissionError("Unauthorized Access. Request is not authorized")

        claims_identity = await JwtTokenValidation.validate_auth_header(
            auth_header, credential_provider, self._get_channel_provider(), channel_id_header
        )

        outbound_audience = (
            JwtTokenValidation.get_app_id_from_claims(claims_identity.claims)
            if SkillValidation.is_skill_claim(claims_identity.claims) else
            self._to_channel_from_bot_oauth_scope
        )

        caller_id = await self.generate_caller_id(
            self._credentials_factory, claims_identity, self._caller_id
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
            credentials_factory=self._credentials_factory,
            http_client_factory=self._http_client_factory,
            logger=self._logger
        )

    async def create_user_token_client(
        self, claims_identity: ClaimsIdentity
    ) -> UserTokenClient:
        pass

    def create_bot_framework_client(self) -> BotFrameworkClient:
        pass

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
            auth_configuration=self._auth_configuration
        )

    def _get_channel_provider(self) -> Optional[ChannelProvider]:
        return (
            SimpleChannelProvider(self._channel_service)
            if self._channel_service is not None else
            None
        )
