# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# from abc import ABC
from typing import Dict, List

from botbuilder.schema import SignInResource, TokenResponse, TokenExchangeRequest
from botframework.connector.token_api.models import TokenStatus
from botframework.connector.auth import AppCredentials

from .turn_context import TurnContext
from .user_token_provider import UserTokenProvider


class ExtendedUserTokenProvider(UserTokenProvider):
    async def get_user_token(
        self,
        turn_context: TurnContext,
        oauth_app_credentials: AppCredentials,
        connection_name: str,
        magic_code: str,
    ) -> TokenResponse:
        """
        Attempts to retrieve the token for a user that's in a login flow, using customized AppCredentials.

        :param turn_context: Context for the current turn of conversation with the user.
        :param oauth_app_credentials: AppCredentials for OAuth.
        :param connection_name: Name of the auth connection to use.
        :param magic_code: (Optional) Optional user entered code to validate.

        :return: Token Response.
        """
        raise NotImplementedError()

    async def get_oauth_sign_in_link(
        self,
        turn_context: TurnContext,
        oauth_app_credentials: AppCredentials,
        connection_name: str,
    ) -> str:
        """
        Get the raw signin link to be sent to the user for signin for a connection name,
        using customized AppCredentials.

        :param turn_context: Context for the current turn of conversation with the user.
        :param oauth_app_credentials: AppCredentials for OAuth.
        :param connection_name: Name of the auth connection to use.


        :return: A task that represents the work queued to execute.
        .. remarks:: If the task completes successfully, the result contains the raw signin link.
        """
        raise NotImplementedError()

    async def get_oauth_sign_in_link_from_user(
        self,
        turn_context: TurnContext,
        oauth_app_credentials: AppCredentials,
        connection_name: str,
        user_id: str,
        final_redirect: str = None,
    ) -> str:
        """
        Get the raw signin link to be sent to the user for signin for a connection name,
        using customized AppCredentials.

        :param turn_context: Context for the current turn of conversation with the user.
        :param oauth_app_credentials: AppCredentials for OAuth.
        :param connection_name: Name of the auth connection to use.
        :param user_id: The user id that will be associated with the token.
        :param final_redirect: The final URL that the OAuth flow will redirect to.


        :return: A task that represents the work queued to execute.
        .. remarks:: If the task completes successfully, the result contains the raw signin link.
        """
        raise NotImplementedError()

    async def sign_out_user(
        self,
        turn_context: TurnContext,
        oauth_app_credentials: AppCredentials,
        connection_name: str = None,
        user_id: str = None,
    ):
        """
        Signs the user out with the token server, using customized AppCredentials.

        :param turn_context: Context for the current turn of conversation with the user.
        :param oauth_app_credentials: AppCredentials for OAuth.
        :param connection_name: Name of the auth connection to use.
        :param user_id: User id of user to sign out.


        :return: A task that represents the work queued to execute.
        """
        raise NotImplementedError()

    async def get_token_status(
        self,
        context: TurnContext,
        oauth_app_credentials: AppCredentials,
        user_id: str,
        include_filter: str = None,
    ) -> List[TokenStatus]:
        """
        Retrieves the token status for each configured connection for the given user, using customized AppCredentials.

        :param context: Context for the current turn of conversation with the user.
        :param oauth_app_credentials: AppCredentials for OAuth.
        :param user_id: The user Id for which token status is retrieved.
        :param include_filter: Optional comma separated list of connection's to include. Blank will return token
        status for all configured connections.


        :return: Array of TokenStatus.
        """
        raise NotImplementedError()

    async def get_aad_tokens(
        self,
        context: TurnContext,
        oauth_app_credentials: AppCredentials,
        connection_name: str,
        resource_urls: List[str],
        user_id: str = None,
    ) -> Dict[str, TokenResponse]:
        """
        Retrieves Azure Active Directory tokens for particular resources on a configured connection,
        using customized AppCredentials.

        :param context: Context for the current turn of conversation with the user.
        :param oauth_app_credentials: AppCredentials for OAuth.
        :param connection_name: The name of the Azure Active Directory connection configured with this bot.
        :param resource_urls: The list of resource URLs to retrieve tokens for.
        :param user_id: The user Id for which tokens are retrieved. If passing in None the user_id is taken from the
        Activity in the ITurnContext.


        :return: Dictionary of resourceUrl to the corresponding TokenResponse.
        """
        raise NotImplementedError()

    async def get_sign_in_resource(
        self, turn_context: TurnContext, connection_name: str
    ) -> SignInResource:
        """
        Get the raw signin link to be sent to the user for signin for a connection name.

        :param turn_context: Context for the current turn of conversation with the user.
        :param connection_name: Name of the auth connection to use.


        :return: A task that represents the work queued to execute.
        .. remarks:: If the task completes successfully, the result contains the raw signin link.
        """
        raise NotImplementedError()

    async def get_sign_in_resource_from_user(
        self,
        turn_context: TurnContext,
        connection_name: str,
        user_id: str,
        final_redirect: str = None,
    ) -> SignInResource:
        """
        Get the raw signin link to be sent to the user for signin for a connection name.

        :param turn_context: Context for the current turn of conversation with the user.
        :param connection_name: Name of the auth connection to use.
        :param user_id: The user id that will be associated with the token.
        :param final_redirect: The final URL that the OAuth flow will redirect to.


        :return: A task that represents the work queued to execute.
        .. remarks:: If the task completes successfully, the result contains the raw signin link.
        """
        raise NotImplementedError()

    async def get_sign_in_resource_from_user_and_credentials(
        self,
        turn_context: TurnContext,
        oauth_app_credentials: AppCredentials,
        connection_name: str,
        user_id: str,
        final_redirect: str = None,
    ) -> SignInResource:
        """
        Get the raw signin link to be sent to the user for signin for a connection name.

        :param turn_context: Context for the current turn of conversation with the user.
        :param oauth_app_credentials: Credentials for OAuth.
        :param connection_name: Name of the auth connection to use.
        :param user_id: The user id that will be associated with the token.
        :param final_redirect: The final URL that the OAuth flow will redirect to.


        :return: A task that represents the work queued to execute.
        .. remarks:: If the task completes successfully, the result contains the raw signin link.
        """
        raise NotImplementedError()

    async def exchange_token(
        self,
        turn_context: TurnContext,
        connection_name: str,
        user_id: str,
        exchange_request: TokenExchangeRequest,
    ) -> TokenResponse:
        """
        Performs a token exchange operation such as for single sign-on.

        :param turn_context: Context for the current turn of conversation with the user.
        :param connection_name: Name of the auth connection to use.
        :param user_id: The user id associated with the token..
        :param exchange_request: The exchange request details, either a token to exchange or a uri to exchange.


        :return: If the task completes, the exchanged token is returned.
        """
        raise NotImplementedError()

    async def exchange_token_from_credentials(
        self,
        turn_context: TurnContext,
        oauth_app_credentials: AppCredentials,
        connection_name: str,
        user_id: str,
        exchange_request: TokenExchangeRequest,
    ) -> TokenResponse:
        """
        Performs a token exchange operation such as for single sign-on.

        :param turn_context: Context for the current turn of conversation with the user.
        :param oauth_app_credentials: AppCredentials for OAuth.
        :param connection_name: Name of the auth connection to use.
        :param user_id: The user id associated with the token..
        :param exchange_request: The exchange request details, either a token to exchange or a uri to exchange.


        :return: If the task completes, the exchanged token is returned.
        """
        raise NotImplementedError()
