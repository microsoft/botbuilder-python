# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC
from typing import Union

from .authentication_configuration import AuthenticationConfiguration
from .authentication_constants import AuthenticationConstants
from .channel_validation import ChannelValidation
from .channel_provider import ChannelProvider
from .claims_identity import ClaimsIdentity
from .credential_provider import CredentialProvider
from .jwt_token_extractor import JwtTokenExtractor
from .verify_options import VerifyOptions


class EnterpriseChannelValidation(ABC):

    TO_BOT_FROM_ENTERPRISE_CHANNEL_TOKEN_VALIDATION_PARAMETERS = VerifyOptions(
        issuer=[AuthenticationConstants.TO_BOT_FROM_CHANNEL_TOKEN_ISSUER],
        audience=None,
        clock_tolerance=5 * 60,
        ignore_expiration=False,
    )

    @staticmethod
    async def authenticate_channel_token(
        auth_header: str,
        credentials: CredentialProvider,
        channel_id: str,
        channel_service_or_provider: Union[str, ChannelProvider],
        auth_configuration: AuthenticationConfiguration = None,
    ) -> ClaimsIdentity:
        channel_service = channel_service_or_provider
        if isinstance(channel_service_or_provider, ChannelProvider):
            channel_service = await channel_service_or_provider.get_channel_service()

        endpoint = (
            ChannelValidation.open_id_metadata_endpoint
            if ChannelValidation.open_id_metadata_endpoint
            else AuthenticationConstants.TO_BOT_FROM_ENTERPRISE_CHANNEL_OPEN_ID_METADATA_URL_FORMAT.replace(
                "{channelService}", channel_service
            )
        )
        token_extractor = JwtTokenExtractor(
            EnterpriseChannelValidation.TO_BOT_FROM_ENTERPRISE_CHANNEL_TOKEN_VALIDATION_PARAMETERS,
            endpoint,
            AuthenticationConstants.ALLOWED_SIGNING_ALGORITHMS,
        )

        identity: ClaimsIdentity = await token_extractor.get_identity_from_auth_header(
            auth_header, channel_id, auth_configuration.required_endorsements
        )
        return await EnterpriseChannelValidation.validate_identity(
            identity, credentials
        )

    @staticmethod
    async def authenticate_channel_token_with_service_url(
        auth_header: str,
        credentials: CredentialProvider,
        service_url: str,
        channel_id: str,
        channel_service_or_provider: Union[str, ChannelProvider],
        auth_configuration: AuthenticationConfiguration = None,
    ) -> ClaimsIdentity:
        identity: ClaimsIdentity = await EnterpriseChannelValidation.authenticate_channel_token(
            auth_header,
            credentials,
            channel_id,
            channel_service_or_provider,
            auth_configuration,
        )

        service_url_claim: str = identity.get_claim_value(
            AuthenticationConstants.SERVICE_URL_CLAIM
        )
        if service_url_claim != service_url:
            raise Exception("Unauthorized. service_url claim do not match.")

        return identity

    @staticmethod
    async def validate_identity(
        identity: ClaimsIdentity, credentials: CredentialProvider
    ) -> ClaimsIdentity:
        if identity is None:
            # No valid identity. Not Authorized.
            raise Exception("Unauthorized. No valid identity.")

        if not identity.is_authenticated:
            # The token is in some way invalid. Not Authorized.
            raise Exception("Unauthorized. Is not authenticated.")

        # Now check that the AppID in the claim set matches
        # what we're looking for. Note that in a multi-tenant bot, this value
        # comes from developer code that may be reaching out to a service, hence the
        # Async validation.

        # Look for the "aud" claim, but only if issued from the Bot Framework
        if (
            identity.get_claim_value(AuthenticationConstants.ISSUER_CLAIM)
            != AuthenticationConstants.TO_BOT_FROM_CHANNEL_TOKEN_ISSUER
        ):
            # The relevant Audience Claim MUST be present. Not Authorized.
            raise Exception("Unauthorized. Issuer claim MUST be present.")

        # The AppId from the claim in the token must match the AppId specified by the developer.
        # In this case, the token is destined for the app, so we find the app ID in the audience claim.
        aud_claim: str = identity.get_claim_value(
            AuthenticationConstants.AUDIENCE_CLAIM
        )
        if not await credentials.is_valid_appid(aud_claim or ""):
            # The AppId is not valid or not present. Not Authorized.
            raise Exception(
                f"Unauthorized. Invalid AppId passed on token: { aud_claim }"
            )

        return identity
