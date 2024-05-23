# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC


class GovernmentConstants(ABC):
    """
    Government Channel Service property value
    """

    CHANNEL_SERVICE = "https://botframework.azure.us"

    """
    TO CHANNEL FROM BOT: Login URL

    DEPRECATED: DO NOT USE
    """
    TO_CHANNEL_FROM_BOT_LOGIN_URL = (
        "https://login.microsoftonline.us/MicrosoftServices.onmicrosoft.us"
    )

    """
    TO CHANNEL FROM BOT: Login URL prefix
    """
    TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX = "https://login.microsoftonline.us/"

    DEFAULT_CHANNEL_AUTH_TENANT = "MicrosoftServices.onmicrosoft.us"

    """
    TO CHANNEL FROM BOT: OAuth scope to request
    """
    TO_CHANNEL_FROM_BOT_OAUTH_SCOPE = "https://api.botframework.us"

    """
    TO BOT FROM CHANNEL: Token issuer
    """
    TO_BOT_FROM_CHANNEL_TOKEN_ISSUER = "https://api.botframework.us"

    """
    OAuth Url used to get a token from OAuthApiClient.
    """
    OAUTH_URL_GOV = "https://api.botframework.azure.us"

    """
    TO BOT FROM CHANNEL: OpenID metadata document for tokens coming from MSA
    """
    TO_BOT_FROM_CHANNEL_OPENID_METADATA_URL = (
        "https://login.botframework.azure.us/v1/.well-known/openidconfiguration"
    )

    """
    TO BOT FROM GOV EMULATOR: OpenID metadata document for tokens coming from MSA
    """
    TO_BOT_FROM_EMULATOR_OPENID_METADATA_URL = (
        "https://login.microsoftonline.us/"
        "cab8a31a-1906-4287-a0d8-4eef66b95f6e/v2.0/"
        ".well-known/openid-configuration"
    )
