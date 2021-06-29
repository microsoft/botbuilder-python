# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from logging import Logger

from ..bot_framework_sdk_client_async import BotFrameworkConnectorConfiguration
from ..http_client_factory import HttpClientFactory

from ._government_cloud_bot_framework_authentication import (
    _GovernmentCloudBotFrameworkAuthentication,
)
from ._parameterized_bot_framework_authentication import (
    _ParameterizedBotFrameworkAuthentication,
)
from ._public_cloud_bot_framework_authentication import (
    _PublicCloudBotFrameworkAuthentication,
)

from .authentication_configuration import AuthenticationConfiguration
from .bot_framework_authentication import BotFrameworkAuthentication
from .government_constants import GovernmentConstants
from .password_service_client_credential_factory import (
    PasswordServiceClientCredentialFactory,
)
from .service_client_credentials_factory import ServiceClientCredentialsFactory


class BotFrameworkAuthenticationFactory:
    @staticmethod
    def create(
        *,
        channel_service: str = None,
        validate_authority: bool = False,
        to_channel_from_bot_login_url: str = None,
        to_channel_from_bot_oauth_scope: str = None,
        to_bot_from_channel_token_issuer: str = None,
        oauth_url: str = None,
        to_bot_from_channel_open_id_metadata_url: str = None,
        to_bot_from_emulator_open_id_metadata_url: str = None,
        caller_id: str = None,
        credential_factory: ServiceClientCredentialsFactory = PasswordServiceClientCredentialFactory(),
        auth_configuration: AuthenticationConfiguration = AuthenticationConfiguration(),
        http_client_factory: HttpClientFactory = None,
        connector_client_configuration: BotFrameworkConnectorConfiguration = None,
        logger: Logger = None
    ) -> BotFrameworkAuthentication:
        """
        Creates the appropriate BotFrameworkAuthentication instance.

        :param channel_service: The Channel Service.
        :param validate_authority: The validate authority value to use.
        :param to_channel_from_bot_login_url: The to Channel from bot login url.
        :param to_channel_from_bot_oauth_scope: The to Channel from bot oauth scope.
        :param to_bot_from_channel_token_issuer: The to bot from Channel Token Issuer.
        :param oauth_url: The oAuth url.
        :param to_bot_from_channel_open_id_metadata_url: The to bot from Channel Open Id Metadata url.
        :param to_bot_from_emulator_open_id_metadata_url: The to bot from Emulator Open Id Metadata url.
        :param caller_id: The Microsoft app password.
        :param credential_factory: The ServiceClientCredentialsFactory to use to create credentials.
        :param auth_configuration: The AuthenticationConfiguration to use.
        :param http_client_factory: The HttpClientFactory to use for a skill BotFrameworkClient.
        :param connector_client_configuration: Configuration to use custom http pipeline for the connector
        :param logger: The Logger to use.
        :return: A new BotFrameworkAuthentication instance.
        """
        # pylint: disable=too-many-boolean-expressions
        if (
            to_channel_from_bot_login_url
            or to_channel_from_bot_oauth_scope
            or to_bot_from_channel_token_issuer
            or oauth_url
            or to_bot_from_channel_open_id_metadata_url
            or to_bot_from_emulator_open_id_metadata_url
            or caller_id
        ):
            # if we have any of the 'parameterized' properties defined we'll assume this is the parameterized code
            return _ParameterizedBotFrameworkAuthentication(
                validate_authority,
                to_channel_from_bot_login_url,
                to_channel_from_bot_oauth_scope,
                to_bot_from_channel_token_issuer,
                oauth_url,
                to_bot_from_channel_open_id_metadata_url,
                to_bot_from_emulator_open_id_metadata_url,
                caller_id,
                credential_factory,
                auth_configuration,
                http_client_factory,
                connector_client_configuration,
                logger,
            )
        # else apply the built in default behavior, which is either the public cloud or the gov cloud
        # depending on whether we have a channelService value present
        if not channel_service:
            return _PublicCloudBotFrameworkAuthentication(
                credential_factory,
                auth_configuration,
                http_client_factory,
                connector_client_configuration,
                logger,
            )
        if channel_service == GovernmentConstants.CHANNEL_SERVICE:
            return _GovernmentCloudBotFrameworkAuthentication(
                credential_factory,
                auth_configuration,
                http_client_factory,
                connector_client_configuration,
                logger,
            )

        # The ChannelService value is used an indicator of which built in set of constants to use.
        # If it is not recognized, a full configuration is expected.
        raise ValueError("The provided channel_service value is not supported.")
