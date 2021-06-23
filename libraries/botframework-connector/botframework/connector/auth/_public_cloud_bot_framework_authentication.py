from logging import Logger

from botbuilder.schema import CallerIdConstants
from botframework.connector import HttpClientFactory
from botframework.connector.auth import (
    ServiceClientCredentialsFactory,
    AuthenticationConfiguration,
    AuthenticationConstants
)
from botframework.connector.auth._built_in_bot_framework_authentication import _BuiltinBotFrameworkAuthentication


class _PublicCloudBotFrameworkAuthentication(_BuiltinBotFrameworkAuthentication):
    def __init__(
        self,
        credentials_factory: ServiceClientCredentialsFactory,
        auth_configuration: AuthenticationConfiguration,
        http_client_factory: HttpClientFactory,
        logger: Logger
    ):
        super(_PublicCloudBotFrameworkAuthentication, self).__init__(
            AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
            AuthenticationConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL,
            CallerIdConstants.public_azure_channel,
            "",  # channel_service
            AuthenticationConstants.OAUTH_URL,
            credentials_factory,
            auth_configuration,
            http_client_factory,
            logger
        )
