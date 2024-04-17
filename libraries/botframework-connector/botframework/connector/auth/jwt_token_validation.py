# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict, List, Union

from botbuilder.schema import Activity, RoleTypes

from ..channels import Channels
from .authentication_configuration import AuthenticationConfiguration
from .authentication_constants import AuthenticationConstants
from .emulator_validation import EmulatorValidation
from .enterprise_channel_validation import EnterpriseChannelValidation
from .channel_validation import ChannelValidation
from .credential_provider import CredentialProvider
from .claims_identity import ClaimsIdentity
from .government_constants import GovernmentConstants
from .government_channel_validation import GovernmentChannelValidation
from .skill_validation import SkillValidation
from .channel_provider import ChannelProvider


class JwtTokenValidation:
    # TODO remove the default value on channel_service
    @staticmethod
    async def authenticate_request(
        activity: Activity,
        auth_header: str,
        credentials: CredentialProvider,
        channel_service_or_provider: Union[str, ChannelProvider] = "",
        auth_configuration: AuthenticationConfiguration = None,
    ) -> ClaimsIdentity:
        """Authenticates the request and sets the service url in the set of trusted urls.
        :param activity: The incoming Activity from the Bot Framework or the Emulator
        :type activity: ~botframework.connector.models.Activity
        :param auth_header: The Bearer token included as part of the request
        :type auth_header: str
        :param credentials: The set of valid credentials, such as the Bot Application ID
        :param channel_service_or_provider: String for the channel service
        :param auth_configuration: Authentication configuration
        :type credentials: CredentialProvider

        :raises Exception:
        """
        if not auth_header:
            # No auth header was sent. We might be on the anonymous code path.
            auth_is_disabled = await credentials.is_authentication_disabled()
            if not auth_is_disabled:
                # No Auth Header. Auth is required. Request is not authorized.
                raise PermissionError("Unauthorized Access. Request is not authorized")

            # Check if the activity is for a skill call and is coming from the Emulator.
            try:
                if (
                    activity.channel_id == Channels.emulator
                    and activity.recipient.role == RoleTypes.skill
                    and activity.relates_to is not None
                ):
                    # Return an anonymous claim with an anonymous skill AppId
                    return SkillValidation.create_anonymous_skill_claim()
            except AttributeError:
                pass

            # In the scenario where Auth is disabled, we still want to have the
            # IsAuthenticated flag set in the ClaimsIdentity. To do this requires
            # adding in an empty claim.
            return ClaimsIdentity({}, True, AuthenticationConstants.ANONYMOUS_AUTH_TYPE)

        # Validate the header and extract claims.
        claims_identity = await JwtTokenValidation.validate_auth_header(
            auth_header,
            credentials,
            channel_service_or_provider,
            activity.channel_id,
            activity.service_url,
            auth_configuration,
        )

        return claims_identity

    @staticmethod
    async def validate_auth_header(
        auth_header: str,
        credentials: CredentialProvider,
        channel_service_or_provider: Union[str, ChannelProvider],
        channel_id: str,
        service_url: str = None,
        auth_configuration: AuthenticationConfiguration = None,
    ) -> ClaimsIdentity:
        if not auth_header:
            raise ValueError("argument auth_header is null")

        async def get_claims() -> ClaimsIdentity:
            if SkillValidation.is_skill_token(auth_header):
                return await SkillValidation.authenticate_channel_token(
                    auth_header,
                    credentials,
                    channel_service_or_provider,
                    channel_id,
                    auth_configuration,
                )

            if EmulatorValidation.is_token_from_emulator(auth_header):
                return await EmulatorValidation.authenticate_emulator_token(
                    auth_header, credentials, channel_service_or_provider, channel_id
                )

            is_public = (
                not channel_service_or_provider
                or isinstance(channel_service_or_provider, ChannelProvider)
                and channel_service_or_provider.is_public_azure()
            )
            is_gov = (
                isinstance(channel_service_or_provider, ChannelProvider)
                and channel_service_or_provider.is_government()
                or isinstance(channel_service_or_provider, str)
                and JwtTokenValidation.is_government(channel_service_or_provider)
            )

            # If the channel is Public Azure
            if is_public:
                if service_url:
                    return await ChannelValidation.authenticate_channel_token_with_service_url(
                        auth_header,
                        credentials,
                        service_url,
                        channel_id,
                        auth_configuration,
                    )

                return await ChannelValidation.authenticate_channel_token(
                    auth_header, credentials, channel_id, auth_configuration
                )

            if is_gov:
                if service_url:
                    return await GovernmentChannelValidation.authenticate_channel_token_with_service_url(
                        auth_header,
                        credentials,
                        service_url,
                        channel_id,
                        auth_configuration,
                    )

                return await GovernmentChannelValidation.authenticate_channel_token(
                    auth_header, credentials, channel_id, auth_configuration
                )

            # Otherwise use Enterprise Channel Validation
            if service_url:
                return await EnterpriseChannelValidation.authenticate_channel_token_with_service_url(
                    auth_header,
                    credentials,
                    service_url,
                    channel_id,
                    channel_service_or_provider,
                    auth_configuration,
                )

            return await EnterpriseChannelValidation.authenticate_channel_token(
                auth_header,
                credentials,
                channel_id,
                channel_service_or_provider,
                auth_configuration,
            )

        claims = await get_claims()

        if claims:
            await JwtTokenValidation.validate_claims(auth_configuration, claims.claims)

        return claims

    @staticmethod
    async def validate_claims(
        auth_config: AuthenticationConfiguration, claims: List[Dict]
    ):
        if auth_config and auth_config.claims_validator:
            await auth_config.claims_validator(claims)
        elif SkillValidation.is_skill_claim(claims):
            # Skill claims must be validated using AuthenticationConfiguration claims_validator
            raise PermissionError(
                "Unauthorized Access. Request is not authorized. Skill Claims require validation."
            )

    @staticmethod
    def is_government(channel_service: str) -> bool:
        return (
            channel_service
            and channel_service.lower() == GovernmentConstants.CHANNEL_SERVICE
        )

    @staticmethod
    def get_app_id_from_claims(claims: Dict[str, object]) -> str:
        app_id = None

        # Depending on Version, the is either in the
        # appid claim (Version 1) or the Authorized Party claim (Version 2).
        token_version = claims.get(AuthenticationConstants.VERSION_CLAIM)

        if not token_version or token_version == "1.0":
            # either no Version or a version of "1.0" means we should look for
            # the claim in the "appid" claim.
            app_id = claims.get(AuthenticationConstants.APP_ID_CLAIM)
        elif token_version == "2.0":
            app_id = claims.get(AuthenticationConstants.AUTHORIZED_PARTY)

        return app_id

    @staticmethod
    def is_valid_token_format(auth_header: str) -> bool:
        if not auth_header:
            # No token. Can't be an emulator token.
            return False

        parts = auth_header.split(" ")
        if len(parts) != 2:
            # Emulator tokens MUST have exactly 2 parts.
            # If we don't have 2 parts, it's not an emulator token
            return False

        auth_scheme = parts[0]

        # The scheme MUST be "Bearer"
        return auth_scheme == "Bearer"
