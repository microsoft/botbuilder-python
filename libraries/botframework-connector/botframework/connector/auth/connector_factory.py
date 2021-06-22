# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from logging import Logger

from botframework.connector import ConnectorClient, HttpClientFactory
from botframework.connector.auth import ServiceClientCredentialsFactory


class ConnectorFactory(ABC):
    @abstractmethod
    async def create(self, service_url: str, audience: str) -> ConnectorClient:
        """
        A factory method used to create ConnectorClient instances.
        :param service_url: The url for the client.
        :param audience: The audience for the credentials the client will use.
        :returns: A ConnectorClient for sending activities to the audience at the service_url.
        """
        raise NotImplementedError()


class _ConnectorFactoryImpl(ConnectorFactory):
    def __init__(
        self,
        app_id: str,
        to_channel_from_bot_oauth_scope: str,
        login_endpoint: str,
        validate_authority: bool,
        credentials_factory: ServiceClientCredentialsFactory,
        http_client_factory: HttpClientFactory,
        logger: Logger
    ):
        self._app_id = app_id
        self._to_channel_from_bot_oauth_scope = to_channel_from_bot_oauth_scope
        self._login_endpoint = login_endpoint
        self._validate_authority = validate_authority
        self._credentials_factory = credentials_factory
        self._http_client_factory = http_client_factory
        self._logger = logger

    async def create(self, service_url: str, audience: str) -> ConnectorClient:
        pass
