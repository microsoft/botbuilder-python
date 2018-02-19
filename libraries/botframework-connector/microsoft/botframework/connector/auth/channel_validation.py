import asyncio

from .verify_options import VerifyOptions
from .constants import Constants
from .jwt_token_extractor import JwtTokenExtractor

class ChannelValidation:
    # This claim is ONLY used in the Channel Validation, and not in the emulator validation
    SERVICE_URL_CLAIM = 'serviceurl'

    #
    # TO BOT FROM CHANNEL: Token validation parameters when connecting to a bot
    #
    TO_BOT_FROM_CHANNEL_TOKEN_VALIDATION_PARAMETERS = VerifyOptions(
        issuer=[Constants.BOT_FRAMEWORK_TOKEN_ISSUER],
        # Audience validation takes place manually in code.
        audience=None,
        clock_tolerance=5 * 60,
        ignore_expiration=False
    )

    @staticmethod
    async def authenticate_token_service_url(auth_header, credentials, service_url):
        identity = await asyncio.ensure_future(
            ChannelValidation.authenticate_token(auth_header, credentials))

        service_url_claim = identity.get_claim_value(ChannelValidation.SERVICE_URL_CLAIM)
        if service_url_claim != service_url:
            # Claim must match. Not Authorized.
            raise Exception('Unauthorized. service_url claim do not match.')

        return identity

    @staticmethod
    async def authenticate_token(auth_header, credentials):
        token_extractor = JwtTokenExtractor(
            ChannelValidation.TO_BOT_FROM_CHANNEL_TOKEN_VALIDATION_PARAMETERS,
            Constants.TO_BOT_FROM_CHANNEL_OPEN_ID_METADATA_URL,
            Constants.ALLOWED_SIGNING_ALGORITHMS)

        identity = await asyncio.ensure_future(
            token_extractor.get_identity_from_auth_header(auth_header))
        if not identity:
            # No valid identity. Not Authorized.
            raise Exception('Unauthorized. No valid identity.')

        if not identity.isAuthenticated:
            # The token is in some way invalid. Not Authorized.
            raise Exception('Unauthorized. Is not authenticated')

        # Now check that the AppID in the claimset matches
        # what we're looking for. Note that in a multi-tenant bot, this value
        # comes from developer code that may be reaching out to a service, hence the
        # Async validation.

        # Look for the "aud" claim, but only if issued from the Bot Framework
        if identity.get_claim_value(Constants.ISSUER_CLAIM) != Constants.BOT_FRAMEWORK_TOKEN_ISSUER:
            # The relevant Audiance Claim MUST be present. Not Authorized.
            raise Exception('Unauthorized. Audiance Claim MUST be present.')

        # The AppId from the claim in the token must match the AppId specified by the developer.
        # Note that the Bot Framwork uses the Audiance claim ("aud") to pass the AppID.
        aud_claim = identity.get_claim_value(Constants.AUDIENCE_CLAIM)
        is_valid_app_id = await asyncio.ensure_future(credentials.is_valid_appid(aud_claim or ""))
        if not is_valid_app_id:
            # The AppId is not valid or not present. Not Authorized.
            raise Exception('Unauthorized. Invalid AppId passed on token: ', aud_claim)

        return identity
