# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict, List

from botbuilder.schema import Activity, TokenResponse

from botframework.connector.token_api import TokenApiClientConfiguration
from botframework.connector.token_api.aio import TokenApiClient
from botframework.connector.token_api.models import (
    SignInUrlResponse,
    TokenExchangeRequest,
    TokenStatus,
)

from .app_credentials import AppCredentials
from .user_token_client import UserTokenClient


class _UserTokenClientImpl(UserTokenClient):
    def __init__(
        self,
        app_id: str,
        credentials: AppCredentials,
        oauth_endpoint: str,
        client_configuration: TokenApiClientConfiguration = None,
    ) -> None:
        super().__init__()
        self._app_id = app_id
        self._client = TokenApiClient(credentials, oauth_endpoint)
        if client_configuration:
            self._client.config = client_configuration

    async def get_user_token(
        self, user_id: str, connection_name: str, channel_id: str, magic_code: str
    ) -> TokenResponse:
        if user_id is None or not isinstance(user_id, str):
            raise TypeError("user_id")
        if connection_name is None or not isinstance(connection_name, str):
            raise TypeError("connection_name")
        if channel_id is None or not isinstance(channel_id, str):
            raise TypeError("channel_id")

        result = await self._client.user_token.get_token(
            user_id, connection_name, channel_id=channel_id, code=magic_code
        )

        if result is None or result.token is None:
            return None

        return result

    async def get_sign_in_resource(
        self, connection_name: str, activity: Activity, final_redirect: str
    ) -> SignInUrlResponse:
        if connection_name is None or not isinstance(connection_name, str):
            raise TypeError("connection_name")
        if activity is None or not isinstance(activity, Activity):
            raise TypeError("activity")

        result = await self._client.bot_sign_in.get_sign_in_resource(
            UserTokenClient.create_token_exchange_state(
                self._app_id, connection_name, activity
            ),
            final_redirect=final_redirect,
        )

        return result

    async def sign_out_user(self, user_id: str, connection_name: str, channel_id: str):
        if user_id is None or not isinstance(user_id, str):
            raise TypeError("user_id")
        if connection_name is None or not isinstance(connection_name, str):
            raise TypeError("connection_name")
        if channel_id is None or not isinstance(channel_id, str):
            raise TypeError("channel_id")

        await self._client.user_token.sign_out(user_id, connection_name, channel_id)

    async def get_token_status(
        self, user_id: str, channel_id: str, include_filter: str
    ) -> List[TokenStatus]:
        if user_id is None or not isinstance(user_id, str):
            raise TypeError("user_id")
        if channel_id is None or not isinstance(channel_id, str):
            raise TypeError("channel_id")

        result = await self._client.user_token.get_token_status(
            user_id, channel_id, include_filter
        )

        return result

    async def get_aad_tokens(
        self,
        user_id: str,
        connection_name: str,
        resource_urls: List[str],
        channel_id: str,
    ) -> Dict[str, TokenResponse]:
        if user_id is None or not isinstance(user_id, str):
            raise TypeError("user_id")
        if connection_name is None or not isinstance(connection_name, str):
            raise TypeError("connection_name")
        if channel_id is None or not isinstance(channel_id, str):
            raise TypeError("channel_id")

        result = await self._client.user_token.get_aad_tokens(
            user_id, connection_name, channel_id, resource_urls
        )

        return result

    async def exchange_token(
        self,
        user_id: str,
        connection_name: str,
        channel_id: str,
        exchange_request: TokenExchangeRequest,
    ) -> TokenResponse:
        if user_id is None or not isinstance(user_id, str):
            raise TypeError("user_id")
        if connection_name is None or not isinstance(connection_name, str):
            raise TypeError("connection_name")
        if channel_id is None or not isinstance(channel_id, str):
            raise TypeError("channel_id")

        (uri, token) = (
            (exchange_request.uri, exchange_request.token)
            if exchange_request
            else (None, None)
        )

        result = await self._client.user_token.exchange_async(
            user_id, connection_name, channel_id, uri, token
        )

        return result
