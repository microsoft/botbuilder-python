# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger

from botbuilder.core import InvokeResponse
from botbuilder.schema import Activity
from botframework.connector import HttpClientFactory
from botframework.connector.auth import ServiceClientCredentialsFactory
from botframework.connector.skills import BotFrameworkClient


class _BotFrameworkClientImpl(BotFrameworkClient):
    def __init__(
        self,
        credentials_factory: ServiceClientCredentialsFactory,
        http_client_factory: HttpClientFactory,
        login_endpoint: str,
        logger: Logger
    ):
        self._credentials_factory = credentials_factory
        self._http_client_factory = http_client_factory
        self._login_endpoint = login_endpoint
        self._logger = logger

    async def post_activity(
        self,
        from_bot_id: str,
        to_bot_id: str,
        to_url: str,
        service_url: str,
        conversation_id: str,
        activity: Activity
    ) -> InvokeResponse:
        pass
