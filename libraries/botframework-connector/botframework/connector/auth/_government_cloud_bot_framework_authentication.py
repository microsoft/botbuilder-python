# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger

from botbuilder.schema import CallerIdConstants

from ..bot_framework_sdk_client_async import BotFrameworkConnectorConfiguration
from ..http_client_factory import HttpClientFactory
from ._built_in_bot_framework_authentication import _BuiltinBotFrameworkAuthentication
from .authentication_configuration import AuthenticationConfiguration
from .government_constants import GovernmentConstants
from .service_client_credentials_factory import ServiceClientCredentialsFactory


class _GovernmentCloudBotFrameworkAuthentication(_BuiltinBotFrameworkAuthentication):
    def __init__(
        self,
        credentials_factory: ServiceClientCredentialsFactory,
        auth_configuration: AuthenticationConfiguration,
        http_client_factory: HttpClientFactory,
        connector_client_configuration: BotFrameworkConnectorConfiguration = None,
        logger: Logger = None,
    ):
        super(_GovernmentCloudBotFrameworkAuthentication, self).__init__(
            GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
            GovernmentConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX,
            CallerIdConstants.us_gov_channel,
            GovernmentConstants.CHANNEL_SERVICE,
            GovernmentConstants.OAUTH_URL_GOV,
            credentials_factory,
            auth_configuration,
            http_client_factory,
            connector_client_configuration,
            logger,
        )
