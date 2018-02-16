class Constants:
    TO_BOT_FROM_EMULATOR_OPEN_ID_METADATA_URL = "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration"
    ALLOWED_SIGNING_ALGORITHMS = [ "RS256", "RS384", "RS512" ]
    AUTHORIZED_PARTY = "azp"
    AUDIENCE_CLAIM = "aud"
    BOT_FRAMEWORK_TOKEN_ISSUER = "https://api.botframework.com"
    TO_BOT_FROM_CHANNEL_OPEN_ID_METADATA_URL = "https://login.botframework.com/v1/.well-known/openidconfiguration"
    ISSUER_CLAIM = "iss"