# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC
from typing import Dict, List

from botframework.connector.token_api.models import (
    SignInUrlResponse,
    TokenExchangeRequest,
    TokenResponse,
)
from botframework.connector.auth import AppCredentials

from botbuilder.core.turn_context import TurnContext
from .user_token_provider import UserTokenProvider


class ExtendedUserTokenProvider(UserTokenProvider, ABC):
    # pylint: disable=unused-argument

    async def get_sign_in_resource(
        self, turn_context: TurnContext, connection_name: str
    ) -> SignInUrlResponse:
        """
        Get the raw signin link to be sent to the user for signin for a connection name.

        :param turn_context: Context for the current turn of conversation with the user.
        :param connection_name: Name of the auth connection to use.


        :return: A task that represents the work queued to execute.
        .. remarks:: If the task completes successfully, the result contains the raw signin link.
        """
        return

    async def get_sign_in_resource_from_user(
        self,
        turn_context: TurnContext,
        connection_name: str,
        user_id: str,
        final_redirect: str = None,
    ) -> SignInUrlResponse:
        """
        Get the raw signin link to be sent to the user for signin for a connection name.

        :param turn_context: Context for the current turn of conversation with the user.
        :param connection_name: Name of the auth connection to use.
        :param user_id: The user id that will be associated with the token.
        :param final_redirect: The final URL that the OAuth flow will redirect to.


        :return: A task that represents the work queued to execute.
        .. remarks:: If the task completes successfully, the result contains the raw signin link.
        """
        return

    async def get_sign_in_resource_from_user_and_credentials(
        self,
        turn_context: TurnContext,
        oauth_app_credentials: AppCredentials,
        connection_name: str,
        user_id: str,
        final_redirect: str = None,
    ) -> SignInUrlResponse:
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
        return

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
        return

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
        return

    async def get_user_token(
        self,
        context: TurnContext,
        connection_name: str,
        magic_code: str = None,
        oauth_app_credentials: AppCredentials = None,
    ) -> TokenResponse:
        """
        Retrieves the OAuth token for a user that is in a sign-in flow.
        :param context:
        :param connection_name:
        :param magic_code:
        :param oauth_app_credentials:
        :return:
        """
        raise NotImplementedError()

    async def sign_out_user(
        self,
        context: TurnContext,
        connection_name: str = None,
        user_id: str = None,
        oauth_app_credentials: AppCredentials = None,
    ):
        """
        Signs the user out with the token server.
        :param context:
        :param connection_name:
        :param user_id:
        :param oauth_app_credentials:
        :return:
        """
        raise NotImplementedError()

    async def get_oauth_sign_in_link(
        self,
        context: TurnContext,
        connection_name: str,
        final_redirect: str = None,
        oauth_app_credentials: AppCredentials = None,
    ) -> str:
        """
        Get the raw signin link to be sent to the user for signin for a connection name.
        :param context:
        :param connection_name:
        :param final_redirect:
        :param oauth_app_credentials:
        :return:
        """
        raise NotImplementedError()

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
        :param context:
        :param connection_name:
        :param resource_urls:
        :param user_id:
        :param oauth_app_credentials:
        :return:
        """
        raise NotImplementedError()
