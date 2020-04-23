# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Optional, Type

from msrest.async_client import SDKClientAsync, ServiceClientAsync
from msrest.universal_http.async_abc import AsyncHTTPSender as AsyncHttpDriver
from msrest.pipeline import AsyncPipeline
from msrest.pipeline.aiohttp import AsyncHTTPSender


from ._configuration import ConnectorClientConfiguration


class BotFrameworkConnectorConfiguration(ConnectorClientConfiguration):
    def __init__(
        self,
        credentials,
        base_url: str,
        *,
        pipeline_type: Optional[Type[AsyncPipeline]] = None,
        sender: Optional[AsyncHTTPSender] = None,
        driver: Optional[AsyncHttpDriver] = None
    ):
        super().__init__(credentials, base_url)

        # The overwrite hierarchy should be well documented
        self.sender = sender
        self.driver = driver

        if pipeline_type:
            self.pipeline = pipeline_type(self)


class BotFrameworkSDKClientAsync(SDKClientAsync):
    def __init__(self, config: BotFrameworkConnectorConfiguration) -> None:
        super().__init__(config)
        self._client = BotFrameworkServiceClientAsync(config)


class BotFrameworkServiceClientAsync(ServiceClientAsync):
    def __init__(self, config: BotFrameworkConnectorConfiguration) -> None:
        super(ServiceClientAsync, self).__init__(config)

        self.config.pipeline = config.pipeline or self._create_default_pipeline()
