# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from datetime import datetime, timedelta
from urllib.parse import urlparse

from adal import AuthenticationContext
import requests

from msrest.authentication import Authentication
from .authentication_constants import AuthenticationConstants

# TODO: Decide to move this to Constants or viceversa (when porting OAuth)
AUTH_SETTINGS = {
    "refreshEndpoint": "https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token",
    "refreshScope": "https://api.botframework.com/.default",
    "botConnectorOpenIdMetadata": "https://login.botframework.com/v1/.well-known/openidconfiguration",
    "botConnectorIssuer": "https://api.botframework.com",
    "emulatorOpenIdMetadata": "https://login.microsoftonline.com/botframework.com/v2.0/"
    ".well-known/openid-configuration",
    "emulatorAuthV31IssuerV1": "https://sts.windows.net/d6d49420-f39b-4df7-a1dc-d59a935871db/",
    "emulatorAuthV31IssuerV2": "https://login.microsoftonline.com/d6d49420-f39b-4df7-a1dc-d59a935871db/v2.0",
    "emulatorAuthV32IssuerV1": "https://sts.windows.net/f8cdef31-a31e-4b4a-93e4-5f571e91255a/",
    "emulatorAuthV32IssuerV2": "https://login.microsoftonline.com/f8cdef31-a31e-4b4a-93e4-5f571e91255a/v2.0",
}


class _OAuthResponse:
    def __init__(self):
        self.token_type = None
        self.expires_in = None
        self.access_token = None
        self.expiration_time = None

    @staticmethod
    def from_json(json_values):
        result = _OAuthResponse()
        try:
            result.token_type = json_values["tokenType"]
            result.access_token = json_values["accessToken"]
            result.expires_in = json_values["expiresIn"]
        except KeyError:
            pass
        return result


class MicrosoftAppCredentials(Authentication):
    """
    MicrosoftAppCredentials auth implementation and cache.
    """

    schema = "Bearer"

    trustedHostNames = {
        "state.botframework.com": datetime.max,
        "api.botframework.com": datetime.max,
        "token.botframework.com": datetime.max,
        "state.botframework.azure.us": datetime.max,
        "api.botframework.azure.us": datetime.max,
        "token.botframework.azure.us": datetime.max,
    }
    cache = {}

    def __init__(
        self,
        app_id: str,
        password: str,
        channel_auth_tenant: str = None,
        oauth_scope: str = None,
    ):
        """
        Initializes a new instance of MicrosoftAppCredentials class
        :param app_id: The Microsoft app ID.
        :param app_password: The Microsoft app password.
        :param channel_auth_tenant: Optional. The oauth token tenant.
        """
        # The configuration property for the Microsoft app ID.
        self.microsoft_app_id = app_id
        # The configuration property for the Microsoft app Password.
        self.microsoft_app_password = password
        tenant = (
            channel_auth_tenant
            if channel_auth_tenant
            else AuthenticationConstants.DEFAULT_CHANNEL_AUTH_TENANT
        )
        self.oauth_endpoint = (
            AuthenticationConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX + tenant
        )
        self.oauth_scope = (
            oauth_scope or AuthenticationConstants.TO_BOT_FROM_CHANNEL_TOKEN_ISSUER
        )
        self.token_cache_key = app_id + self.oauth_scope + "-cache" if app_id else None
        self.authentication_context = AuthenticationContext(self.oauth_endpoint)

    # pylint: disable=arguments-differ
    def signed_session(self, session: requests.Session = None) -> requests.Session:
        """
        Gets the signed session.
        :returns: Signed requests.Session object
        """
        if not session:
            session = requests.Session()

        # If there is no microsoft_app_id and no self.microsoft_app_password, then there shouldn't
        # be an "Authorization" header on the outgoing activity.
        if not self.microsoft_app_id and not self.microsoft_app_password:
            session.headers.pop("Authorization", None)

        elif not session.headers.get("Authorization"):
            auth_token = self.get_access_token()
            header = "{} {}".format("Bearer", auth_token)
            session.headers["Authorization"] = header

        return session

    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        Gets an OAuth access token.
        :param force_refresh: True to force a refresh of the token; or false to get
                              a cached token if it exists.
        :returns: Access token string
        """
        if self.microsoft_app_id and self.microsoft_app_password:
            if not force_refresh:
                # check the global cache for the token. If we have it, and it's valid, we're done.
                oauth_token = MicrosoftAppCredentials.cache.get(
                    self.token_cache_key, None
                )
                if oauth_token is not None:
                    # we have the token. Is it valid?
                    if oauth_token.expiration_time > datetime.now():
                        return oauth_token.access_token
            # We need to refresh the token, because:
            #   1. The user requested it via the force_refresh parameter
            #   2. We have it, but it's expired
            #   3. We don't have it in the cache.
            oauth_token = self.refresh_token()
            MicrosoftAppCredentials.cache.setdefault(self.token_cache_key, oauth_token)
            return oauth_token.access_token
        return ""

    def refresh_token(self) -> _OAuthResponse:
        """
        returns: _OAuthResponse
        """

        token = self.authentication_context.acquire_token_with_client_credentials(
            self.oauth_scope, self.microsoft_app_id, self.microsoft_app_password
        )

        oauth_response = _OAuthResponse.from_json(token)
        oauth_response.expiration_time = datetime.now() + timedelta(
            seconds=(int(oauth_response.expires_in) - 300)
        )

        return oauth_response

    @staticmethod
    def trust_service_url(service_url: str, expiration=None):
        """
        Checks if the service url is for a trusted host or not.
        :param service_url: The service url.
        :param expiration: The expiration time after which this service url is not trusted anymore.
        :returns: True if the host of the service url is trusted; False otherwise.
        """
        if expiration is None:
            expiration = datetime.now() + timedelta(days=1)
        host = urlparse(service_url).hostname
        if host is not None:
            MicrosoftAppCredentials.trustedHostNames[host] = expiration

    @staticmethod
    def is_trusted_service(service_url: str) -> bool:
        """
        Checks if the service url is for a trusted host or not.
        :param service_url: The service url.
        :returns: True if the host of the service url is trusted; False otherwise.
        """
        host = urlparse(service_url).hostname
        if host is not None:
            return MicrosoftAppCredentials._is_trusted_url(host)
        return False

    @staticmethod
    def _is_trusted_url(host: str) -> bool:
        expiration = MicrosoftAppCredentials.trustedHostNames.get(host, datetime.min)
        return expiration > (datetime.now() - timedelta(minutes=5))
