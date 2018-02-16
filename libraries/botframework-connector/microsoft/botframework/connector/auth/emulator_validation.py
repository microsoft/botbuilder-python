import jwt

from .credential_provider import CredentialProvider 
from .jwt_token_extractor import JwtTokenExtractor

class VerifyOptions:
    def __init__(self, issuer, audience, clock_tolerance, ignore_expiration):
        self.issuer = issuer
        self.audience = audience
        self.clock_tolerance = clock_tolerance
        self.ignore_expiration = ignore_expiration

class EmulatorValidation:
    APP_ID_CLAIM = "appid"
    VERSION_CLAIM = "ver"
    TO_BOT_FROM_EMULATOR_TOKEN_VALIDATION_PARAMETERS = VerifyOptions(
        issuer = [
            'https://sts.windows.net/d6d49420-f39b-4df7-a1dc-d59a935871db/',                   # Auth v3.1, 1.0 token
            'https://login.microsoftonline.com/d6d49420-f39b-4df7-a1dc-d59a935871db/v2.0',     # Auth v3.1, 2.0 token
            'https://sts.windows.net/f8cdef31-a31e-4b4a-93e4-5f571e91255a/',                   # Auth v3.2, 1.0 token
            'https://login.microsoftonline.com/f8cdef31-a31e-4b4a-93e4-5f571e91255a/v2.0',     # Auth v3.2, 2.0 token
            'https://sts.windows.net/72f988bf-86f1-41af-91ab-2d7cd011db47/'                    # ???
        ],
        audience = None,
        clock_tolerance = 5 * 60,
        ignore_expiration = False
    )

    @staticmethod
    def is_from_emulator(authHeader):
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
    def authenticate_token(header, credentials):
        pass