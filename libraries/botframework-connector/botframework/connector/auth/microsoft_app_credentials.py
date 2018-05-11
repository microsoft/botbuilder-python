from datetime import datetime, timedelta
from urllib.parse import urlparse

from msrest.authentication import (
    BasicTokenAuthentication,
    Authentication)
import requests

AUTH_SETTINGS = {
    "refreshEndpoint": 'https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token',
    "refreshScope": 'https://api.botframework.com/.default',
    "botConnectorOpenIdMetadata":
        'https://login.botframework.com/v1/.well-known/openidconfiguration',
    "botConnectorIssuer": 'https://api.botframework.com',
    "emulatorOpenIdMetadata":
        'https://login.microsoftonline.com/botframework.com/v2.0/.well-known/openid-configuration',
    "emulatorAuthV31IssuerV1": 'https://sts.windows.net/d6d49420-f39b-4df7-a1dc-d59a935871db/',
    "emulatorAuthV31IssuerV2":
        'https://login.microsoftonline.com/d6d49420-f39b-4df7-a1dc-d59a935871db/v2.0',
    "emulatorAuthV32IssuerV1": 'https://sts.windows.net/f8cdef31-a31e-4b4a-93e4-5f571e91255a/',
    "emulatorAuthV32IssuerV2":
        'https://login.microsoftonline.com/f8cdef31-a31e-4b4a-93e4-5f571e91255a/v2.0'
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
            result.token_type = json_values["token_type"]
            result.access_token = json_values["access_token"]
            result.expires_in = json_values["expires_in"]
        except KeyError:
            pass
        return result


class MicrosoftAppCredentials(Authentication):
    refreshEndpoint = AUTH_SETTINGS["refreshEndpoint"]
    refreshScope = AUTH_SETTINGS["refreshScope"]
    schema = 'Bearer'

    trustedHostNames = {}
    cache = {}

    def __init__(self, appId: str, password: str):
        self.microsoft_app_id = appId
        self.microsoft_app_password = password
        self.token_cache_key = appId + '-cache'

    def signed_session(self):
        basic_authentication = BasicTokenAuthentication({"access_token": self.get_access_token()})
        session = basic_authentication.signed_session()

        # If there is no microsoft_app_id and no self.microsoft_app_password, then there shouldn't
        # be an "Authorization" header on the outgoing activity.
        if not self.microsoft_app_id and not self.microsoft_app_password:
            del session.headers['Authorization']
        return session

    def get_access_token(self, force_refresh=False):
        if self.microsoft_app_id and self.microsoft_app_password:
            if not force_refresh:
                # check the global cache for the token. If we have it, and it's valid, we're done.
                oauth_token = MicrosoftAppCredentials.cache.get(self.token_cache_key, None)
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
        else:
            return ''

    def refresh_token(self):
        options = {
            'grant_type': 'client_credentials',
            'client_id': self.microsoft_app_id,
            'client_secret': self.microsoft_app_password,
            'scope': MicrosoftAppCredentials.refreshScope}
        response = requests.post(MicrosoftAppCredentials.refreshEndpoint, data=options)
        response.raise_for_status()
        oauth_response = _OAuthResponse.from_json(response.json())
        oauth_response.expiration_time = datetime.now() + \
                                        timedelta(seconds=(oauth_response.expires_in - 300))
        return oauth_response

    @staticmethod
    def trust_service_url(service_url: str, expiration=None):
        if expiration is None:
            expiration = datetime.now() + timedelta(days=1)
        host = urlparse(service_url).hostname
        if host is not None:
            MicrosoftAppCredentials.trustedHostNames[host] = expiration

    @staticmethod
    def is_trusted_service(service_url: str) -> bool:
        host = urlparse(service_url).hostname
        if host is not None:
            return MicrosoftAppCredentials.is_trusted_url(host)
        return False

    @staticmethod
    def is_trusted_url(host: str) -> bool:
        expiration = MicrosoftAppCredentials.trustedHostNames.get(host, datetime.min)
        return expiration > (datetime.now() - timedelta(minutes=5))
