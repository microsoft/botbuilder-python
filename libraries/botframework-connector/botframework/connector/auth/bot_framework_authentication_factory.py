# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botframework.connector import BotFrameworkConnectorConfiguration

from .authentication_configuration import AuthenticationConfiguration
from .bot_framework_authentication import BotFrameworkAuthentication
from .service_client_credentials_factory import ServiceClientCredentialsFactory


class BotFrameworkAuthenticationFactory:
    @staticmethod
    def create(
        *,
        channel_service: str = None,
        validate_authority: bool = None,
        to_channel_from_bot_login_url: str = None,
        to_channel_from_bot_oauth_scope: str = None,
        to_bot_from_channel_token_issuer: str = None,
        oauth_url: str = None,
        to_bot_from_channel_open_id_metadata_url: str = None,
        to_bot_from_emulator_open_id_metadata_url: str = None,
        caller_id: str = None,
        credential_factory: ServiceClientCredentialsFactory = None,
        auth_configuration: AuthenticationConfiguration = None,
        connector_client_options: BotFrameworkConnectorConfiguration = None
    ) -> BotFrameworkAuthentication:
        pass
