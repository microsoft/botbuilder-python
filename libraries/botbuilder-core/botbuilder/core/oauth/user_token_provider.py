# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from typing import Dict, List

from botbuilder.core.turn_context import TurnContext
from botbuilder.schema import TokenResponse
from botframework.connector.auth import AppCredentials


class UserTokenProvider(ABC):
    @abstractmethod
    async def get_user_token(
        self,
        context: TurnContext,
        connection_name: str,
        magic_code: str = None,
        oauth_app_credentials: AppCredentials = None,
    ) -> TokenResponse:
        """
        Retrieves the OAuth token for a user that is in a sign-in flow.
        :param context: Context for the current turn of conversation with the user.
        :param connection_name: Name of the auth connection to use.
        :param magic_code: (Optional) Optional user entered code to validate.
        :param oauth_app_credentials: (Optional) AppCredentials for OAuth.  If None is supplied, the
        Bots credentials are used.
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def sign_out_user(
        self,
        context: TurnContext,
        connection_name: str = None,
        user_id: str = None,
        oauth_app_credentials: AppCredentials = None,
    ):
        """
        Signs the user out with the token server.
        :param context: Context for the current turn of conversation with the user.
        :param connection_name: Name of the auth connection to use.
        :param user_id: User id of user to sign out.
        :param oauth_app_credentials: (Optional) AppCredentials for OAuth.  If None is supplied, the
        Bots credentials are used.
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_oauth_sign_in_link(
        self,
        context: TurnContext,
        connection_name: str,
        final_redirect: str = None,
        oauth_app_credentials: AppCredentials = None,
    ) -> str:
        """
        Get the raw signin link to be sent to the user for signin for a connection name.
        :param context: Context for the current turn of conversation with the user.
        :param connection_name: Name of the auth connection to use.
        :param final_redirect: The final URL that the OAuth flow will redirect to.
        :param oauth_app_credentials: (Optional) AppCredentials for OAuth.  If None is supplied, the
        Bots credentials are used.
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_token_status(
        self,
        context: TurnContext,
        connection_name: str = None,
        user_id: str = None,
        include_filter: str = None,
        oauth_app_credentials: AppCredentials = None,
    ) -> Dict[str, TokenResponse]:
        """
        Retrieves Azure Active Directory tokens for particular resources on a configured connection.
        :param context: Context for the current turn of conversation with the user.
        :param connection_name: Name of the auth connection to use.
        :param user_id: The user Id for which token status is retrieved.
        :param include_filter: Optional comma separated list of connection's to include. Blank will return token status
        for all configured connections.
        :param oauth_app_credentials: (Optional) AppCredentials for OAuth.  If None is supplied, the
        Bots credentials are used.
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_aad_tokens(
        self,
        context: TurnContext,
        connection_name: str,
        resource_urls: List[str],
        user_id: str = None,
        oauth_app_credentials: AppCredentials = None,
    ) -> Dict[str, TokenResponse]:
        """
        Retrieves Azure Active Directory tokens for particular resources on a configured connection.
        :param context: Context for the current turn of conversation with the user.
        :param connection_name: Name of the auth connection to use.
        :param resource_urls: The list of resource URLs to retrieve tokens for.
        :param user_id: The user Id for which tokens are retrieved. If passing in None the userId is taken
        from the Activity in the TurnContext.
        :param oauth_app_credentials: (Optional) AppCredentials for OAuth.  If None is supplied, the
        Bots credentials are used.
        :return:
        """
        raise NotImplementedError()
