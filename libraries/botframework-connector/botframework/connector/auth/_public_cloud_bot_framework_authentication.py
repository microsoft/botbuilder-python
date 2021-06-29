# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger

from botbuilder.schema import CallerIdConstants

from ..bot_framework_sdk_client_async import BotFrameworkConnectorConfiguration
from ..http_client_factory import HttpClientFactory

from .service_client_credentials_factory import ServiceClientCredentialsFactory
from .authentication_configuration import AuthenticationConfiguration
from .authentication_constants import AuthenticationConstants
from ._built_in_bot_framework_authentication import _BuiltinBotFrameworkAuthentication


class _PublicCloudBotFrameworkAuthentication(_BuiltinBotFrameworkAuthentication):
    def __init__(
        self,
        credentials_factory: ServiceClientCredentialsFactory,
        auth_configuration: AuthenticationConfiguration,
        http_client_factory: HttpClientFactory,
        connector_client_configuration: BotFrameworkConnectorConfiguration = None,
        logger: Logger = None,
    ):
        super(_PublicCloudBotFrameworkAuthentication, self).__init__(
            AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
            AuthenticationConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX,
            CallerIdConstants.public_azure_channel,
            "",  # channel_service
            AuthenticationConstants.OAUTH_URL,
            credentials_factory,
            auth_configuration,
            http_client_factory,
            connector_client_configuration,
            logger,
        )
