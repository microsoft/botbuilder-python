import asyncio

from .verify_options import VerifyOptions
from .constants import Constants
from .credential_provider import CredentialProvider
from .claims_identity import ClaimsIdentity
from .jwt_token_extractor import JwtTokenExtractor

class ChannelValidation:
    # This claim is ONLY used in the Channel Validation, and not in the emulator validation
    SERVICE_URL_CLAIM = 'serviceurl'

    #
    # TO BOT FROM CHANNEL: Token validation parameters when connecting to a bot
    #
    TO_BOT_FROM_CHANNEL_TOKEN_VALIDATION_PARAMETERS = VerifyOptions(
        issuer = [Constants.BOT_FRAMEWORK_TOKEN_ISSUER],
        # Audience validation takes place manually in code.
        audience = None,
        clock_tolerance = 5 * 60,
        ignore_expiration = False
    )
    
    @staticmethod
    async def authenticate_channel_token_with_service_url(authHeader, credentials, serviceUrl):
        identity = await asyncio.ensure_future(ChannelValidation.authenticate_channel_token(authHeader, credentials))

        serviceUrlClaim = identity.getClaimValue(ChannelValidation.SERVICE_URL_CLAIM)
        if (serviceUrlClaim != serviceUrl):
            # Claim must match. Not Authorized.
            raise Exception('Unauthorized. ServiceUrl claim do not match.')

        return identity

    @staticmethod
    async def authenticate_channel_token(authHeader, credentials):
        tokenExtractor = JwtTokenExtractor(
            ChannelValidation.TO_BOT_FROM_CHANNEL_TOKEN_VALIDATION_PARAMETERS,
            Constants.TO_BOT_FROM_CHANNEL_OPEN_ID_METADATA_URL,
            Constants.ALLOWED_SIGNING_ALGORITHMS)

        identity = await asyncio.ensure_future(tokenExtractor.get_identity_from_auth_header(authHeader))
        if (not identity):
            # No valid identity. Not Authorized.
            raise Exception('Unauthorized. No valid identity.')

        if (not identity.isAuthenticated):
            # The token is in some way invalid. Not Authorized.
            raise Exception('Unauthorized. Is not authenticated')

        # Now check that the AppID in the claimset matches
        # what we're looking for. Note that in a multi-tenant bot, this value
        # comes from developer code that may be reaching out to a service, hence the
        # Async validation.

        # Look for the "aud" claim, but only if issued from the Bot Framework
        if (identity.getClaimValue(Constants.ISSUER_CLAIM) != Constants.BOT_FRAMEWORK_TOKEN_ISSUER):
            # The relevant Audiance Claim MUST be present. Not Authorized.
            raise Exception('Unauthorized. Audiance Claim MUST be present.')

        # The AppId from the claim in the token must match the AppId specified by the developer. Note that
        # the Bot Framwork uses the Audiance claim ("aud") to pass the AppID.
        audClaim = identity.getClaimValue(Constants.AUDIENCE_CLAIM)
        isValidAppId = await asyncio.ensure_future(credentials.isValidAppId(audClaim or ""))
        if (not isValidAppId):
            # The AppId is not valid or not present. Not Authorized.
            raise Exception('Unauthorized. Invalid AppId passed on token: ', audClaim)

        return identity