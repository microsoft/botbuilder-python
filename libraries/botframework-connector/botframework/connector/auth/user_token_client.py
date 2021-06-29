# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from base64 import b64encode
from json import dumps
from typing import Dict, List

from botbuilder.schema import Activity, TokenResponse, TokenExchangeState

from botframework.connector.token_api.models import (
    SignInUrlResponse,
    TokenExchangeRequest,
    TokenStatus,
)


class UserTokenClient(ABC):
    @abstractmethod
    async def get_user_token(
        self, user_id: str, connection_name: str, channel_id: str, magic_code: str
    ) -> TokenResponse:
        """
        Attempts to retrieve the token for a user that's in a login flow.

        :param user_id: The user id that will be associated with the token.
        :param connection_name: Name of the auth connection to use.
        :param channel_id: The channel Id that will be associated with the token.
        :param magic_code: (Optional) Optional user entered code to validate.
        :return: A TokenResponse object.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_sign_in_resource(
        self, connection_name: str, activity: Activity, final_redirect: str
    ) -> SignInUrlResponse:
        """
        Get the raw signin link to be sent to the user for signin for a connection name.

        :param connection_name: Name of the auth connection to use.
        :param activity: The Activity from which to derive the token exchange state.
        :param final_redirect: The final URL that the OAuth flow will redirect to.
        :return: A SignInUrlResponse.
        """
        raise NotImplementedError()

    @abstractmethod
    async def sign_out_user(self, user_id: str, connection_name: str, channel_id: str):
        """
        Signs the user out with the token server.

        :param user_id: The user id that will be associated with the token.
        :param connection_name: Name of the auth connection to use.
        :param channel_id: The channel Id that will be associated with the token.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_token_status(
        self, user_id: str, channel_id: str, include_filter: str
    ) -> List[TokenStatus]:
        """
        Retrieves the token status for each configured connection for the given user.

        :param user_id: The user id that will be associated with the token.
        :param channel_id: The channel Id that will be associated with the token.
        :param include_filter: The include filter.
        :return: A list of TokenStatus objects.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_aad_tokens(
        self,
        user_id: str,
        connection_name: str,
        resource_urls: List[str],
        channel_id: str,
    ) -> Dict[str, TokenResponse]:
        """
        Retrieves Azure Active Directory tokens for particular resources on a configured connection.

        :param user_id: The user id that will be associated with the token.
        :param connection_name: Name of the auth connection to use.
        :param resource_urls: The list of resource URLs to retrieve tokens for.
        :param channel_id: The channel Id that will be associated with the token.
        :return: A Dictionary of resource_urls to the corresponding TokenResponse.
        """
        raise NotImplementedError()

    @abstractmethod
    async def exchange_token(
        self,
        user_id: str,
        connection_name: str,
        channel_id: str,
        exchange_request: TokenExchangeRequest,
    ) -> TokenResponse:
        """
        Performs a token exchange operation such as for single sign-on.

        :param user_id The user id that will be associated with the token.
        :param connection_name Name of the auth connection to use.
        :param channel_id The channel Id that will be associated with the token.
        :param exchange_request The exchange request details, either a token to exchange or a uri to exchange.
        :return: A TokenResponse object.
        """
        raise NotImplementedError()

    @staticmethod
    def create_token_exchange_state(
        app_id: str, connection_name: str, activity: Activity
    ) -> str:
        """
        Helper function to create the Base64 encoded token exchange state used in getSignInResource calls.

        :param app_id The app_id to include in the token exchange state.
        :param connection_name The connection_name to include in the token exchange state.
        :param activity The [Activity](xref:botframework-schema.Activity) from which to derive the token exchange state.
        :return: Base64 encoded token exchange state.
        """
        if app_id is None or not isinstance(app_id, str):
            raise TypeError("app_id")
        if connection_name is None or not isinstance(connection_name, str):
            raise TypeError("connection_name")
        if activity is None or not isinstance(activity, Activity):
            raise TypeError("activity")

        token_exchange_state = TokenExchangeState(
            connection_name=connection_name,
            conversation=Activity.get_conversation_reference(activity),
            relates_to=activity.relates_to,
            ms_app_id=app_id,
        )

        tes_string = b64encode(
            dumps(token_exchange_state.serialize()).encode(
                encoding="UTF-8", errors="strict"
            )
        ).decode()

        return tes_string
