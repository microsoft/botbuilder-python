# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC


class AuthenticationConstants(ABC):
    # TO CHANNEL FROM BOT: Login URL
    #
    # DEPRECATED: DO NOT USE
    TO_CHANNEL_FROM_BOT_LOGIN_URL = (
        "https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token"
    )

    # TO CHANNEL FROM BOT: Login URL prefix
    TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX = "https://login.microsoftonline.com/"

    # TO CHANNEL FROM BOT: Login URL token endpoint path
    TO_CHANNEL_FROM_BOT_TOKEN_ENDPOINT_PATH = "/oauth2/v2.0/token"

    # TO CHANNEL FROM BOT: Default tenant from which to obtain a token for bot to channel communication
    DEFAULT_CHANNEL_AUTH_TENANT = "botframework.com"

    # TO CHANNEL FROM BOT: OAuth scope to request
    TO_CHANNEL_FROM_BOT_OAUTH_SCOPE = "https://api.botframework.com"

    # TO BOT FROM CHANNEL: Token issuer
    TO_BOT_FROM_CHANNEL_TOKEN_ISSUER = "https://api.botframework.com"

    """
    OAuth Url used to get a token from OAuthApiClient.
    """
    OAUTH_URL = "https://api.botframework.com"

    # Application Setting Key for the OpenIdMetadataUrl value.
    BOT_OPEN_ID_METADATA_KEY = "BotOpenIdMetadata"

    # Application Setting Key for the ChannelService value.
    CHANNEL_SERVICE = "ChannelService"

    # Application Setting Key for the OAuthUrl value.
    OAUTH_URL_KEY = "OAuthApiEndpoint"

    # Application Settings Key for whether to emulate OAuthCards when using the emulator.
    EMULATE_OAUTH_CARDS_KEY = "EmulateOAuthCards"

    # TO BOT FROM CHANNEL: OpenID metadata document for tokens coming from MSA
    TO_BOT_FROM_CHANNEL_OPENID_METADATA_URL = (
        "https://login.botframework.com/v1/.well-known/openidconfiguration"
    )

    # TO BOT FROM ENTERPRISE CHANNEL: OpenID metadata document for tokens coming from MSA
    TO_BOT_FROM_ENTERPRISE_CHANNEL_OPEN_ID_METADATA_URL_FORMAT = (
        "https://{channelService}.enterprisechannel.botframework.com"
        "/v1/.well-known/openidconfiguration"
    )

    # TO BOT FROM EMULATOR: OpenID metadata document for tokens coming from MSA
    TO_BOT_FROM_EMULATOR_OPENID_METADATA_URL = (
        "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration"
    )

    # The V1 Azure AD token issuer URL template that will contain the tenant id where
    # the token was issued from.
    VALID_TOKEN_ISSUER_URL_TEMPLATE_V1 = "https://sts.windows.net/{0}/"

    # The V2 Azure AD token issuer URL template that will contain the tenant id where
    # the token was issued from.
    VALID_TOKEN_ISSUER_URL_TEMPLATE_V2 = "https://login.microsoftonline.com/{0}/v2.0"

    # The Government V1 Azure AD token issuer URL template that will contain the tenant id
    # where the token was issued from.
    VALID_GOVERNMENT_TOKEN_ISSUER_URL_TEMPLATE_V1 = (
        "https://login.microsoftonline.us/{0}/"
    )

    # The Government V2 Azure AD token issuer URL template that will contain the tenant id
    # where the token was issued from.
    VALID_GOVERNMENT_TOKEN_ISSUER_URL_TEMPLATE_V2 = (
        "https://login.microsoftonline.us/{0}/v2.0"
    )

    # Allowed token signing algorithms. Tokens come from channels to the bot. The code
    # that uses this also supports tokens coming from the emulator.
    ALLOWED_SIGNING_ALGORITHMS = ["RS256", "RS384", "RS512"]

    # "azp" Claim.
    # Authorized party - the party to which the ID Token was issued.
    # This claim follows the general format set forth in the OpenID Spec.
    #     http://openid.net/specs/openid-connect-core-1_0.html#IDToken
    AUTHORIZED_PARTY = "azp"

    """
    Audience Claim. From RFC 7519.
        https://tools.ietf.org/html/rfc7519#section-4.1.3
    The "aud" (audience) claim identifies the recipients that the JWT is
    intended for.  Each principal intended to process the JWT MUST
    identify itself with a value in the audience claim.If the principal
    processing the claim does not identify itself with a value in the
    "aud" claim when this claim is present, then the JWT MUST be
    rejected.In the general case, the "aud" value is an array of case-
    sensitive strings, each containing a StringOrURI value.In the
    special case when the JWT has one audience, the "aud" value MAY be a
    single case-sensitive string containing a StringOrURI value.The
    interpretation of audience values is generally application specific.
    Use of this claim is OPTIONAL.
    """
    AUDIENCE_CLAIM = "aud"

    """
    Issuer Claim. From RFC 7519.
        https://tools.ietf.org/html/rfc7519#section-4.1.1
    The "iss" (issuer) claim identifies the principal that issued the
    JWT.  The processing of this claim is generally application specific.
    The "iss" value is a case-sensitive string containing a StringOrURI
    value.  Use of this claim is OPTIONAL.
    """
    ISSUER_CLAIM = "iss"

    """
    From RFC 7515
        https://tools.ietf.org/html/rfc7515#section-4.1.4
    The "kid" (key ID) Header Parameter is a hint indicating which key
    was used to secure the JWS. This parameter allows originators to
    explicitly signal a change of key to recipients. The structure of
    the "kid" value is unspecified. Its value MUST be a case-sensitive
    string. Use of this Header Parameter is OPTIONAL.
    When used with a JWK, the "kid" value is used to match a JWK "kid"
    parameter value.
    """
    KEY_ID_HEADER = "kid"

    # Token version claim name. As used in Microsoft AAD tokens.
    VERSION_CLAIM = "ver"

    # App ID claim name. As used in Microsoft AAD 1.0 tokens.
    APP_ID_CLAIM = "appid"

    # Service URL claim name. As used in Microsoft Bot Framework v3.1 auth.
    SERVICE_URL_CLAIM = "serviceurl"

    # AppId used for creating skill claims when there is no appId and password configured.
    ANONYMOUS_SKILL_APP_ID = "AnonymousSkill"

    # Indicates that ClaimsIdentity.authentication_type is anonymous (no app Id and password were provided).
    ANONYMOUS_AUTH_TYPE = "anonymous"
