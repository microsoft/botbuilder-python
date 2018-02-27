class Constants: # pylint: disable=too-few-public-methods
    TO_BOT_FROM_CHANNEL_TOKEN_ISSUER = "https://api.botframework.com"

    TO_BOT_FROM_EMULATOR_OPEN_ID_METADATA_URL = (
        "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration")
    TO_BOT_FROM_CHANNEL_OPEN_ID_METADATA_URL = (
        "https://login.botframework.com/v1/.well-known/openidconfiguration")

    ALLOWED_SIGNING_ALGORITHMS = ["RS256", "RS384", "RS512"]
    
    AUTHORIZED_PARTY = "azp"
    AUDIENCE_CLAIM = "aud"
    ISSUER_CLAIM = "iss"
