# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import requests
from msrest.authentication import Authentication

from .authentication_constants import AuthenticationConstants


class AppCredentials(Authentication):
    """
    Base class for token retrieval.  Subclasses MUST override get_access_token in
    order to supply a valid token for the specific credentials.
    """

    schema = "Bearer"
    cache = {}
    __tenant = None

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
        self.microsoft_app_id = app_id
        self.tenant = channel_auth_tenant
        self.oauth_endpoint = (
            self._get_to_channel_from_bot_loginurl_prefix() + self.tenant
        )
        self.oauth_scope = oauth_scope or self._get_to_channel_from_bot_oauthscope()

    def _get_default_channelauth_tenant(self) -> str:
        return AuthenticationConstants.DEFAULT_CHANNEL_AUTH_TENANT

    def _get_to_channel_from_bot_loginurl_prefix(self) -> str:
        return AuthenticationConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX

    def _get_to_channel_from_bot_oauthscope(self) -> str:
        return AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE

    @property
    def tenant(self) -> str:
        return self.__tenant

    @tenant.setter
    def tenant(self, value: str):
        self.__tenant = value or self._get_default_channelauth_tenant()

    @staticmethod
    def trust_service_url(service_url: str, expiration=None):
        """
        Obsolete: trust_service_url is not a required part of the security model.
        Checks if the service url is for a trusted host or not.
        :param service_url: The service url.
        :param expiration: The expiration time after which this service url is not trusted anymore.
        """

    @staticmethod
    def is_trusted_service(service_url: str) -> bool:  # pylint: disable=unused-argument
        """
        Obsolete: is_trusted_service is not a required part of the security model.
        Checks if the service url is for a trusted host or not.
        :param service_url: The service url.
        :returns: True if the host of the service url is trusted; False otherwise.
        """
        return True

    @staticmethod
    def _is_trusted_url(host: str) -> bool:  # pylint: disable=unused-argument
        """
        Obsolete: _is_trusted_url is not a required part of the security model.
        """
        return True

    # pylint: disable=arguments-differ
    def signed_session(self, session: requests.Session = None) -> requests.Session:
        """
        Gets the signed session.  This is called by the msrest package
        :returns: Signed requests.Session object
        """
        if not session:
            session = requests.Session()

        if not self._should_set_token(session):
            session.headers.pop("Authorization", None)
        else:
            auth_token = self.get_access_token()
            header = "{} {}".format("Bearer", auth_token)
            session.headers["Authorization"] = header

        return session

    def _should_set_token(
        self, session: requests.Session  # pylint: disable=unused-argument
    ) -> bool:
        # We don't set the token if the AppId is not set, since it means that we are in an un-authenticated scenario.
        return (
            self.microsoft_app_id != AuthenticationConstants.ANONYMOUS_SKILL_APP_ID
            and self.microsoft_app_id
        )

    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        Returns a token for the current AppCredentials.
        :return: The token
        """
        raise NotImplementedError()
