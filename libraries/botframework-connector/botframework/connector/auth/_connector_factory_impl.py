# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger

from botframework.connector.aio import ConnectorClient

from ..about import __version__
from ..bot_framework_sdk_client_async import BotFrameworkConnectorConfiguration
from .connector_factory import ConnectorFactory
from .service_client_credentials_factory import ServiceClientCredentialsFactory

USER_AGENT = f"Microsoft-BotFramework/3.1 (BotBuilder Python/{__version__})"


class _ConnectorFactoryImpl(ConnectorFactory):
    def __init__(
        self,
        app_id: str,
        to_channel_from_bot_oauth_scope: str,
        login_endpoint: str,
        validate_authority: bool,
        credential_factory: ServiceClientCredentialsFactory,
        connector_client_configuration: BotFrameworkConnectorConfiguration = None,
        logger: Logger = None,
    ) -> None:
        self._app_id = app_id
        self._to_channel_from_bot_oauth_scope = to_channel_from_bot_oauth_scope
        self._login_endpoint = login_endpoint
        self._validate_authority = validate_authority
        self._credential_factory = credential_factory
        self._connector_client_configuration = connector_client_configuration
        self._logger = logger

    async def create(self, service_url: str, audience: str = None) -> ConnectorClient:
        # Use the credentials factory to create credentails specific to this particular cloud environment.
        credentials = await self._credential_factory.create_credentials(
            self._app_id,
            audience or self._to_channel_from_bot_oauth_scope,
            self._login_endpoint,
            self._validate_authority,
        )

        # A new connector client for making calls against this serviceUrl using credentials derived
        # from the current appId and the specified audience.
        if self._connector_client_configuration:
            client = ConnectorClient(
                credentials,
                base_url=service_url,
                custom_configuration=self._connector_client_configuration,
            )
        else:
            client = ConnectorClient(credentials, base_url=service_url)
        client.config.add_user_agent(USER_AGENT)
        return client
