# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger
from typing import Dict, Optional

from botbuilder.schema import Activity, RoleTypes

from ..bot_framework_sdk_client_async import BotFrameworkConnectorConfiguration
from ..http_client_factory import HttpClientFactory
from ..channels import Channels
from ..skills.bot_framework_client import BotFrameworkClient

from .bot_framework_authentication import BotFrameworkAuthentication
from .claims_identity import ClaimsIdentity
from .user_token_client import UserTokenClient
from .connector_factory import ConnectorFactory
from .authenticate_request_result import AuthenticateRequestResult
from .service_client_credentials_factory import ServiceClientCredentialsFactory
from .authentication_configuration import AuthenticationConfiguration
from .verify_options import VerifyOptions
from .jwt_token_validation import JwtTokenValidation
from .skill_validation import SkillValidation
from .authentication_constants import AuthenticationConstants
from .emulator_validation import EmulatorValidation
from .jwt_token_extractor import JwtTokenExtractor
from ._bot_framework_client_impl import _BotFrameworkClientImpl
from ._built_in_bot_framework_authentication import _BuiltinBotFrameworkAuthentication
from ._user_token_client_impl import _UserTokenClientImpl
from ._connector_factory_impl import _ConnectorFactoryImpl


class _ParameterizedBotFrameworkAuthentication(BotFrameworkAuthentication):
    def __init__(
        self,
        validate_authority: bool,
        to_channel_from_bot_login_url: str,
        to_channel_from_bot_oauth_scope: str,
        to_bot_from_channel_token_issuer: str,
        oauth_url: str,
        to_bot_from_channel_open_id_metadata_url: str,
        to_bot_from_emulator_open_id_metadata_url: str,
        caller_id: str,
        credentials_factory: ServiceClientCredentialsFactory,
        auth_configuration: AuthenticationConfiguration,
        http_client_factory: HttpClientFactory,
        connector_client_configuration: BotFrameworkConnectorConfiguration = None,
        logger: Logger = None,
    ):
        self._validate_authority = validate_authority
        self._to_channel_from_bot_login_url = to_channel_from_bot_login_url
        self._to_channel_from_bot_oauth_scope = to_channel_from_bot_oauth_scope
        self._to_bot_from_channel_token_issuer = to_bot_from_channel_token_issuer
        self._oauth_url = oauth_url
        self._to_bot_from_channel_open_id_metadata_url = (
            to_bot_from_channel_open_id_metadata_url
        )
        self._to_bot_from_emulator_open_id_metadata_url = (
            to_bot_from_emulator_open_id_metadata_url
        )
        self._caller_id = caller_id
        self._credentials_factory = credentials_factory
        self._auth_configuration = auth_configuration
        self._http_client_factory = http_client_factory
        self._connector_client_configuration = connector_client_configuration
        self._logger = logger

    async def authenticate_request(
        self, activity: Activity, auth_header: str
    ) -> AuthenticateRequestResult:
        claims_identity = await self._jwt_token_validation_authenticate_request(
            activity, auth_header
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
            login_endpoint=self._to_channel_from_bot_login_url,
            validate_authority=self._validate_authority,
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
        if channel_id_header is None:
            is_auth_disabled = (
                await self._credentials_factory.is_authentication_disabled()
            )
            if not is_auth_disabled:
                raise PermissionError("Unauthorized Access. Request is not authorized")

        claims_identity = await self._jwt_token_validation_validate_auth_header(
            auth_header, channel_id_header
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
            login_endpoint=self._to_channel_from_bot_login_url,
            validate_authority=self._validate_authority,
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
            login_endpoint=self._to_channel_from_bot_login_url,
            validate_authority=self._validate_authority,
        )

        return _UserTokenClientImpl(app_id, credentials, self._oauth_url)

    def create_bot_framework_client(self) -> BotFrameworkClient:
        return _BotFrameworkClientImpl(
            self._credentials_factory,
            self._http_client_factory,
            self._to_channel_from_bot_login_url,
            self._logger,
        )

    def get_originating_audience(self) -> str:
        return self._to_channel_from_bot_oauth_scope

    async def authenticate_channel_request(self, auth_header: str) -> ClaimsIdentity:
        return await self._jwt_token_validation_validate_auth_header(
            auth_header, channel_id="unknown"
        )

    async def _jwt_token_validation_authenticate_request(
        self, activity: Activity, auth_header: str
    ) -> ClaimsIdentity:
        if auth_header is None:
            is_auth_disabled = (
                await self._credentials_factory.is_authentication_disabled()
            )
            if not is_auth_disabled:
                # No Auth Header. Auth is required. Request is not authorized.
                raise PermissionError("Unauthorized Access. Request is not authorized")

            # Check if the activity is for a skill call and is coming from the Emulator.
            if (
                activity.channel_id == Channels.emulator
                and activity.recipient.role == RoleTypes.skill
            ):
                # Return an anonymous claim with an anonymous skill AppId
                return SkillValidation.create_anonymous_skill_claim()

            # In the scenario where Auth is disabled, we still want to have the
            # IsAuthenticated flag set in the ClaimsIdentity. To do this requires
            # adding in an empty claim.
            return ClaimsIdentity({}, True, AuthenticationConstants.ANONYMOUS_AUTH_TYPE)

        # Validate the header and extract claims.
        claims_identity = await self._jwt_token_validation_validate_auth_header(
            auth_header, activity.channel_id, activity.service_url
        )

        return claims_identity

    async def _jwt_token_validation_validate_auth_header(
        self, auth_header: str, channel_id: str, service_url: Optional[str] = None
    ) -> ClaimsIdentity:
        identity = await self._jwt_token_validation_authenticate_token(
            auth_header, channel_id, service_url
        )

        await self._jwt_token_validation_validate_claims(identity.claims)

        return identity

    async def _jwt_token_validation_validate_claims(self, claims: Dict[str, object]):
        if self._auth_configuration.claims_validator:
            # Call the validation method if defined (it should throw an exception if the validation fails)
            await self._auth_configuration.claims_validator([claims])
        elif SkillValidation.is_skill_claim(claims):
            raise PermissionError(
                "ClaimsValidator is required for validation of Skill Host calls."
            )

    async def _jwt_token_validation_authenticate_token(
        self, auth_header: str, channel_id: str, service_url: str
    ) -> ClaimsIdentity:
        if SkillValidation.is_skill_token(auth_header):
            return await self._skill_validation_authenticate_channel_token(
                auth_header, channel_id
            )

        if EmulatorValidation.is_token_from_emulator(auth_header):
            return await self._emulator_validation_authenticate_emulator_token(
                auth_header, channel_id
            )

        return await self._government_channel_validation_authenticate_channel_token(
            auth_header, service_url, channel_id
        )

    # // The following code is based on SkillValidation.authenticate_channel_token
    async def _skill_validation_authenticate_channel_token(
        self, auth_header: str, channel_id: str
    ) -> Optional[ClaimsIdentity]:
        if not auth_header:
            return None

        validation_params = VerifyOptions(
            issuer=[
                # TODO: presumably this table should also come from configuration
                # Auth v3.1, 1.0 token
                "https://sts.windows.net/d6d49420-f39b-4df7-a1dc-d59a935871db/",
                # Auth v3.1, 2.0 token
                "https://login.microsoftonline.com/d6d49420-f39b-4df7-a1dc-d59a935871db/v2.0",
                # Auth v3.2, 1.0 token
                "https://sts.windows.net/f8cdef31-a31e-4b4a-93e4-5f571e91255a/",
                # Auth v3.2, 2.0 token
                "https://login.microsoftonline.com/f8cdef31-a31e-4b4a-93e4-5f571e91255a/v2.0",
                # Auth for US Gov, 1.0 token
                "https://sts.windows.net/cab8a31a-1906-4287-a0d8-4eef66b95f6e/",
                # Auth for US Gov, 2.0 token
                "https://login.microsoftonline.us/cab8a31a-1906-4287-a0d8-4eef66b95f6e/v2.0",
            ],
            audience=None,  # Audience validation takes place manually in code.
            clock_tolerance=5 * 60,
            ignore_expiration=False,
        )

        if self._auth_configuration.valid_token_issuers:
            validation_params.issuer.append(
                self._auth_configuration.valid_token_issuers
            )

        # TODO: what should the openIdMetadataUrl be here?
        token_extractor = JwtTokenExtractor(
            validation_params,
            metadata_url=self._to_bot_from_emulator_open_id_metadata_url,
            allowed_algorithms=AuthenticationConstants.ALLOWED_SIGNING_ALGORITHMS,
        )

        parts = auth_header.split(" ")
        if len(parts) != 2:
            return None

        identity = await token_extractor.get_identity(
            schema=parts[0],
            parameter=parts[1],
            channel_id=channel_id,
            required_endorsements=self._auth_configuration.required_endorsements,
        )

        await self._skill_validation_validate_identity(identity)

        return identity

    async def _skill_validation_validate_identity(self, identity: ClaimsIdentity):
        if identity is None:
            # No valid identity. Not Authorized.
            raise PermissionError("Invalid Identity")

        if not identity.is_authenticated:
            # The token is in some way invalid. Not Authorized.
            raise PermissionError("Token Not Authenticated")

        version_claim = identity.get_claim_value(AuthenticationConstants.VERSION_CLAIM)
        if not version_claim:
            # No version claim
            raise PermissionError(
                f"'{AuthenticationConstants.VERSION_CLAIM}' claim is required on skill Tokens."
            )

        # Look for the "aud" claim, but only if issued from the Bot Framework
        audience_claim = identity.get_claim_value(
            AuthenticationConstants.AUDIENCE_CLAIM
        )
        if not audience_claim:
            # Claim is not present or doesn't have a value. Not Authorized.
            raise PermissionError(
                f"'{AuthenticationConstants.AUDIENCE_CLAIM}' claim is required on skill Tokens."
            )

        is_valid_app_id = await self._credentials_factory.is_valid_app_id(
            audience_claim
        )
        if not is_valid_app_id:
            # The AppId is not valid. Not Authorized.
            raise PermissionError("Invalid audience.")

        app_id = JwtTokenValidation.get_app_id_from_claims(identity.claims)
        if not app_id:
            # Invalid appId
            raise PermissionError("Invalid appId.")

    # The following code is based on EmulatorValidation.authenticate_emulator_token
    async def _emulator_validation_authenticate_emulator_token(
        self, auth_header: str, channel_id: str
    ) -> Optional[ClaimsIdentity]:
        if not auth_header:
            return None

        to_bot_from_emulator_validation_params = VerifyOptions(
            issuer=[
                # TODO: presumably this table should also come from configuration
                # Auth v3.1, 1.0 token
                "https://sts.windows.net/d6d49420-f39b-4df7-a1dc-d59a935871db/",
                # Auth v3.1, 2.0 token
                "https://login.microsoftonline.com/d6d49420-f39b-4df7-a1dc-d59a935871db/v2.0",
                # Auth v3.2, 1.0 token
                "https://sts.windows.net/f8cdef31-a31e-4b4a-93e4-5f571e91255a/",
                # Auth v3.2, 2.0 token
                "https://login.microsoftonline.com/f8cdef31-a31e-4b4a-93e4-5f571e91255a/v2.0",
                # Auth for US Gov, 1.0 token
                "https://sts.windows.net/cab8a31a-1906-4287-a0d8-4eef66b95f6e/",
                # Auth for US Gov, 2.0 token
                "https://login.microsoftonline.us/cab8a31a-1906-4287-a0d8-4eef66b95f6e/v2.0",
            ],
            audience=None,  # Audience validation takes place manually in code.
            clock_tolerance=5 * 60,
            ignore_expiration=False,
        )

        if self._auth_configuration.valid_token_issuers:
            to_bot_from_emulator_validation_params.issuer.append(
                self._auth_configuration.valid_token_issuers
            )

        token_extractor = JwtTokenExtractor(
            to_bot_from_emulator_validation_params,
            metadata_url=self._to_bot_from_emulator_open_id_metadata_url,
            allowed_algorithms=AuthenticationConstants.ALLOWED_SIGNING_ALGORITHMS,
        )

        parts = auth_header.split(" ")
        if len(parts) != 2:
            return None

        identity = await token_extractor.get_identity(
            schema=parts[0],
            parameter=parts[1],
            channel_id=channel_id,
            required_endorsements=self._auth_configuration.required_endorsements,
        )

        if identity is None:
            # No valid identity. Not Authorized.
            raise PermissionError("Invalid Identity")

        if not identity.is_authenticated:
            # The token is in some way invalid. Not Authorized.
            raise PermissionError("Token Not Authenticated")

        # Now check that the AppID in the claim set matches
        # what we're looking for. Note that in a multi-tenant bot, this value
        # comes from developer code that may be reaching out to a service, hence the
        # Async validation.
        version_claim = identity.get_claim_value(AuthenticationConstants.VERSION_CLAIM)
        if version_claim is None:
            raise PermissionError("'ver' claim is required on Emulator Tokens.")

        # The Emulator, depending on Version, sends the AppId via either the
        # appid claim (Version 1) or the Authorized Party claim (Version 2).
        if not version_claim or version_claim == "1.0":
            # either no Version or a version of "1.0" means we should look for
            # the claim in the "appid" claim.
            app_id = identity.get_claim_value(AuthenticationConstants.APP_ID_CLAIM)
            if not app_id:
                # No claim around AppID. Not Authorized.
                raise PermissionError(
                    "'appid' claim is required on Emulator Token version '1.0'."
                )
        elif version_claim == "2.0":
            app_id = identity.get_claim_value(AuthenticationConstants.AUTHORIZED_PARTY)
            if not app_id:
                raise PermissionError(
                    "'azp' claim is required on Emulator Token version '2.0'."
                )
        else:
            # Unknown Version. Not Authorized.
            raise PermissionError(f"Unknown Emulator Token version '{version_claim}'.")

        is_valid_app_id = await self._credentials_factory.is_valid_app_id(app_id)
        if not is_valid_app_id:
            raise PermissionError(f"Invalid AppId passed on token: {app_id}")

        return identity

    async def _government_channel_validation_authenticate_channel_token(
        self, auth_header: str, service_url: str, channel_id: str
    ) -> Optional[ClaimsIdentity]:
        if not auth_header:
            return None

        validation_params = VerifyOptions(
            issuer=[self._to_bot_from_channel_token_issuer],
            audience=None,  # Audience validation takes place in JwtTokenExtractor
            clock_tolerance=5 * 60,
            ignore_expiration=False,
        )

        token_extractor = JwtTokenExtractor(
            validation_params,
            metadata_url=self._to_bot_from_channel_open_id_metadata_url,
            allowed_algorithms=AuthenticationConstants.ALLOWED_SIGNING_ALGORITHMS,
        )

        parts = auth_header.split(" ")
        if len(parts) != 2:
            return None

        identity = await token_extractor.get_identity(
            schema=parts[0],
            parameter=parts[1],
            channel_id=channel_id,
            required_endorsements=self._auth_configuration.required_endorsements,
        )

        await self._government_channel_validation_validate_identity(
            identity, service_url
        )

        return identity

    async def _government_channel_validation_validate_identity(
        self, identity: ClaimsIdentity, service_url: str
    ):
        if identity is None:
            # No valid identity. Not Authorized.
            raise PermissionError()

        if not identity.is_authenticated:
            # The token is in some way invalid. Not Authorized.
            raise PermissionError()

        # Now check that the AppID in the claim set matches
        # what we're looking for. Note that in a multi-tenant bot, this value
        # comes from developer code that may be reaching out to a service, hence the
        # Async validation.

        # Look for the "aud" claim, but only if issued from the Bot Framework
        issuer = identity.get_claim_value(AuthenticationConstants.ISSUER_CLAIM)
        if issuer != self._to_bot_from_channel_token_issuer:
            raise PermissionError()

        app_id = identity.get_claim_value(AuthenticationConstants.AUDIENCE_CLAIM)
        if not app_id:
            # The relevant audience Claim MUST be present. Not Authorized.
            raise PermissionError()

        # The AppId from the claim in the token must match the AppId specified by the developer.
        # In this case, the token is destined for the app, so we find the app ID in the audience claim.
        is_valid_app_id = await self._credentials_factory.is_valid_app_id(app_id)
        if not is_valid_app_id:
            # The AppId is not valid. Not Authorized.
            raise PermissionError(f"Invalid AppId passed on token: {app_id}")

        if service_url is not None:
            service_url_claim = identity.get_claim_value(
                AuthenticationConstants.SERVICE_URL_CLAIM
            )
            if not service_url_claim:
                # Claim must be present. Not Authorized.
                raise PermissionError()

            if service_url_claim != service_url:
                # Claim must match. Not Authorized.
                raise PermissionError()
