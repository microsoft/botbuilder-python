# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC

from botbuilder.core import TurnContext
from botbuilder.core.bot_framework_adapter import TokenExchangeRequest
from botbuilder.core.oauth import ConnectorClientBuilder, ExtendedUserTokenProvider
from botbuilder.schema import TokenResponse
from botframework.connector import ConnectorClient
from botframework.connector.auth import ClaimsIdentity, ConnectorFactory
from botframework.connector.auth.user_token_client import UserTokenClient
from botframework.connector.token_api.models import SignInUrlResponse

from .prompts.oauth_prompt_settings import OAuthPromptSettings


class _UserTokenAccess(ABC):
    @staticmethod
    async def get_user_token(
        turn_context: TurnContext, settings: OAuthPromptSettings, magic_code: str
    ) -> TokenResponse:
        user_token_client: UserTokenClient = turn_context.turn_state.get(
            UserTokenClient.__name__, None
        )
        if user_token_client:
            return await user_token_client.get_user_token(
                turn_context.activity.from_property.id,
                settings.connection_name,
                turn_context.activity.channel_id,
                magic_code,
            )
        if isinstance(turn_context.adapter, ExtendedUserTokenProvider):
            return await turn_context.adapter.get_user_token(
                turn_context,
                settings.connection_name,
                magic_code,
                settings.oath_app_credentials,
            )

        raise TypeError("OAuthPrompt is not supported by the current adapter")

    @staticmethod
    async def get_sign_in_resource(
        turn_context: TurnContext, settings: OAuthPromptSettings
    ) -> SignInUrlResponse:
        user_token_client: UserTokenClient = turn_context.turn_state.get(
            UserTokenClient.__name__, None
        )
        if user_token_client:
            return await user_token_client.get_sign_in_resource(
                settings.connection_name, turn_context.activity, None
            )
        if isinstance(turn_context.adapter, ExtendedUserTokenProvider):
            return await turn_context.adapter.get_sign_in_resource_from_user_and_credentials(
                turn_context,
                settings.oath_app_credentials,
                settings.connection_name,
                (
                    turn_context.activity.from_property.id
                    if turn_context.activity and turn_context.activity.from_property
                    else None
                ),
            )

        raise TypeError("OAuthPrompt is not supported by the current adapter")

    @staticmethod
    async def sign_out_user(turn_context: TurnContext, settings: OAuthPromptSettings):
        user_token_client: UserTokenClient = turn_context.turn_state.get(
            UserTokenClient.__name__, None
        )
        if user_token_client:
            return await user_token_client.sign_out_user(
                turn_context.activity.from_property.id,
                settings.connection_name,
                turn_context.activity.channel_id,
            )
        if isinstance(turn_context.adapter, ExtendedUserTokenProvider):
            return await turn_context.adapter.sign_out_user(
                turn_context,
                settings.connection_name,
                (
                    turn_context.activity.from_property.id
                    if turn_context.activity and turn_context.activity.from_property
                    else None
                ),
                settings.oath_app_credentials,
            )

        raise TypeError("OAuthPrompt is not supported by the current adapter")

    @staticmethod
    async def exchange_token(
        turn_context: TurnContext,
        settings: OAuthPromptSettings,
        token_exchange_request: TokenExchangeRequest,
    ) -> TokenResponse:
        user_token_client: UserTokenClient = turn_context.turn_state.get(
            UserTokenClient.__name__, None
        )
        user_id = turn_context.activity.from_property.id
        if user_token_client:
            channel_id = turn_context.activity.channel_id
            return await user_token_client.exchange_token(
                user_id,
                channel_id,
                token_exchange_request,
            )
        if isinstance(turn_context.adapter, ExtendedUserTokenProvider):
            return await turn_context.adapter.exchange_token(
                turn_context,
                settings.connection_name,
                user_id,
                token_exchange_request,
            )

        raise TypeError("OAuthPrompt is not supported by the current adapter")

    @staticmethod
    async def create_connector_client(
        turn_context: TurnContext,
        service_url: str,
        claims_identity: ClaimsIdentity,
        audience: str,
    ) -> ConnectorClient:
        connector_factory: ConnectorFactory = turn_context.turn_state.get(
            ConnectorFactory.__name__, None
        )
        if connector_factory:
            return await connector_factory.create(service_url, audience)
        if isinstance(turn_context.adapter, ConnectorClientBuilder):
            return await turn_context.adapter.create_connector_client(
                service_url,
                claims_identity,
                audience,
            )

        raise TypeError("OAuthPrompt is not supported by the current adapter")
