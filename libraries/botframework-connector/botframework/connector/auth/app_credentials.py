# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datetime import datetime, timedelta
from urllib.parse import urlparse

import requests
from msrest.authentication import Authentication

from botframework.connector.auth import AuthenticationConstants


class AppCredentials(Authentication):
    """
    Base class for token retrieval.  Subclasses MUST override get_access_token in
    order to supply a valid token for the specific credentials.
    """

    schema = "Bearer"

    trustedHostNames = {
        # "state.botframework.com": datetime.max,
        # "state.botframework.azure.us": datetime.max,
        "api.botframework.com": datetime.max,
        "token.botframework.com": datetime.max,
        "api.botframework.azure.us": datetime.max,
        "token.botframework.azure.us": datetime.max,
    }
    cache = {}

    def __init__(
        self,
        app_id: str = None,
        channel_auth_tenant: str = None,
        oauth_scope: str = None,
    ):
        """
        Initializes a new instance of MicrosoftAppCredentials class
        :param channel_auth_tenant: Optional. The oauth token tenant.
        """
        tenant = (
            channel_auth_tenant
            if channel_auth_tenant
            else AuthenticationConstants.DEFAULT_CHANNEL_AUTH_TENANT
        )
        self.oauth_endpoint = (
            AuthenticationConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX + tenant
        )
        self.oauth_scope = (
            oauth_scope or AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
        )

        self.microsoft_app_id = app_id

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
            AppCredentials.trustedHostNames[host] = expiration

    @staticmethod
    def is_trusted_service(service_url: str) -> bool:
        """
        Checks if the service url is for a trusted host or not.
        :param service_url: The service url.
        :returns: True if the host of the service url is trusted; False otherwise.
        """
        host = urlparse(service_url).hostname
        if host is not None:
            return AppCredentials._is_trusted_url(host)
        return False

    @staticmethod
    def _is_trusted_url(host: str) -> bool:
        expiration = AppCredentials.trustedHostNames.get(host, datetime.min)
        return expiration > (datetime.now() - timedelta(minutes=5))

    # pylint: disable=arguments-differ
    def signed_session(self, session: requests.Session = None) -> requests.Session:
        """
        Gets the signed session.  This is called by the msrest package
        :returns: Signed requests.Session object
        """
        if not session:
            session = requests.Session()

        if not self._should_authorize(session):
            session.headers.pop("Authorization", None)
        else:
            auth_token = self.get_access_token()
            header = "{} {}".format("Bearer", auth_token)
            session.headers["Authorization"] = header

        return session

    def _should_authorize(
        self, session: requests.Session  # pylint: disable=unused-argument
    ) -> bool:
        # We don't set the token if the AppId is not set, since it means that we are in an un-authenticated scenario.
        return (
            self.microsoft_app_id != AuthenticationConstants.ANONYMOUS_SKILL_APP_ID
            and self.microsoft_app_id is not None
        )

    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        Returns a token for the current AppCredentials.
        :return: The token
        """
        raise NotImplementedError()
