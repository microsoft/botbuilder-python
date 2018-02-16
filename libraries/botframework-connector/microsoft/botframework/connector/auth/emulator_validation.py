import asyncio
import jwt

from .credential_provider import CredentialProvider 
from .jwt_token_extractor import JwtTokenExtractor
from .verify_options import VerifyOptions
from .constants import Constants

class EmulatorValidation:
    APP_ID_CLAIM = "appid"
    VERSION_CLAIM = "ver"
    TO_BOT_FROM_EMULATOR_TOKEN_VALIDATION_PARAMETERS = VerifyOptions(
        issuer=[
            # Auth v3.1, 1.0 token
            'https://sts.windows.net/d6d49420-f39b-4df7-a1dc-d59a935871db/',
            # Auth v3.1, 2.0 token
            'https://login.microsoftonline.com/d6d49420-f39b-4df7-a1dc-d59a935871db/v2.0',
            # Auth v3.2, 1.0 token
            'https://sts.windows.net/f8cdef31-a31e-4b4a-93e4-5f571e91255a/',
            # Auth v3.2, 2.0 token
            'https://login.microsoftonline.com/f8cdef31-a31e-4b4a-93e4-5f571e91255a/v2.0',
            # ???
            'https://sts.windows.net/72f988bf-86f1-41af-91ab-2d7cd011db47/'
        ],
        audience=None,
        clock_tolerance=5 * 60,
        ignore_expiration=False
    )

    @staticmethod
    def is_token_from_emulator(authHeader):
        """Determines if a given Auth header is from the Bot Framework Emulator
        authHeader Bearer Token, in the "Bearer [Long String]" Format.
        returns True, if the token was issued by the Emulator. Otherwise, false.
        """

        # The Auth Header generally looks like this:
        # "Bearer eyJ0e[...Big Long String...]XAiO"
        if (not authHeader):
            # No token. Can't be an emulator token.
            return False

        parts = authHeader.split(' ')
        if (parts.length != 2):
            # Emulator tokens MUST have exactly 2 parts. If we don't have 2 parts, it's not an emulator token
            return False

        authScheme = parts[0]
        bearerToken = parts[1]

        # We now have an array that should be:
        # [0] = "Bearer"
        # [1] = "[Big Long String]"
        if (authScheme != 'Bearer'):
            # The scheme from the emulator MUST be "Bearer"
            return False

        # Parse the Big Long String into an actual token.
        token = jwt.decode(bearerToken, verify=False)
        if (not token):
            return False

        # Is there an Issuer?
        issuer = token.payload.iss
        if (not issuer):
            # No Issuer, means it's not from the Emulator.
            return False

        # Is the token issues by a source we consider to be the emulator?
        if (EmulatorValidation.TO_BOT_FROM_EMULATOR_TOKEN_VALIDATION_PARAMETERS.issuer and EmulatorValidation.TO_BOT_FROM_EMULATOR_TOKEN_VALIDATION_PARAMETERS.issuer.find(issuer) == -1):
            # Not a Valid Issuer. This is NOT a Bot Framework Emulator Token.
            return False

        # The Token is from the Bot Framework Emulator. Success!
        return True

    @staticmethod
    async def authenticate_emulator_token(authHeader, credentials):
        """Validate the incoming Auth Header as a token sent from the Bot Framework Emulator.
        A token issued by the Bot Framework will FAIL this check. Only Emulator tokens will pass.
        authHeader The raw HTTP header in the format: "Bearer [longString]"
        credentials The user defined set of valid credentials, such as the AppId.
        returns A valid ClaimsIdentity.
        """

        tokenExtractor = JwtTokenExtractor(
            EmulatorValidation.TO_BOT_FROM_EMULATOR_TOKEN_VALIDATION_PARAMETERS,
            Constants.TO_BOT_FROM_EMULATOR_OPEN_ID_METADATA_URL,
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
        versionClaim = identity.get_claim_value(EmulatorValidation.VERSION_CLAIM)
        if (versionClaim == None):
            raise Exception('Unauthorized. "ver" claim is required on Emulator Tokens.')

        appId= ''

        # The Emulator, depending on Version, sends the AppId via either the
        # appid claim (Version 1) or the Authorized Party claim (Version 2).
        if (not versionClaim or versionClaim == '1.0'):
            # either no Version or a version of "1.0" means we should look for
            # the claim in the "appid" claim.
            appIdClaim = identity.get_claim_value(EmulatorValidation.APP_ID_CLAIM)
            if (not appIdClaim):
                # No claim around AppID. Not Authorized.
                raise Exception('Unauthorized. "appid" claim is required on Emulator Token version "1.0".')

            appId = appIdClaim
        elif (versionClaim == '2.0'):
            # Emulator, "2.0" puts the AppId in the "azp" claim.
            appZClaim = identity.get_claim_value(Constants.AUTHORIZED_PARTY)
            if (not appZClaim):
                # No claim around AppID. Not Authorized.
                raise Exception('Unauthorized. "azp" claim is required on Emulator Token version "2.0".')

            appId = appZClaim
        elif (versionClaim == '3.0'):
            # The v3.0 Token types have been disallowed. Not Authorized.
            raise Exception('Unauthorized. Emulator token version "3.0" is depricated.')
        elif (versionClaim == '3.1' or versionClaim == '3.2'):
            # The emulator for token versions "3.1" & "3.2" puts the AppId in the "Audiance" claim.
            audianceClaim = identity.getClaimValue(Constants.AUDIENCE_CLAIM)
            if (not audianceClaim):
                # No claim around AppID. Not Authorized.
                raise Exception('Unauthorized. "aud" claim is required on Emulator Token version "3.x".')

            appId = audianceClaim
        else:
            # Unknown Version. Not Authorized.
            raise Exception('Unauthorized. Unknown Emulator Token version ', versionClaim, '.')

        isValidAppId = await asyncio.ensure_future(credentials.isValidAppId(appId))
        if (not isValidAppId):
            raise Exception('Unauthorized. Invalid AppId passed on token: ', appId)

        return identity
