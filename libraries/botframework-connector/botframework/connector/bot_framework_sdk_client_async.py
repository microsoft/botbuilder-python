# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Optional, Type

from msrest.async_client import SDKClientAsync, ServiceClientAsync
from msrest.pipeline import AsyncPipeline


from ._configuration import ConnectorClientConfiguration


class BotFrameworkConnectorConfiguration(ConnectorClientConfiguration):
    def __init__(
        self,
        credentials,
        base_url: str,
        *,
        pipeline: Optional[Type[AsyncPipeline]] = None
    ):
        super().__init__(credentials, base_url)

        if pipeline:
            self.pipeline = pipeline(self)


class BotFrameworkSDKClientAsync(SDKClientAsync):
    def __init__(self, config: BotFrameworkConnectorConfiguration) -> None:
        super().__init__(config)
        self._client = BotFrameworkServiceClientAsync(config)


class BotFrameworkServiceClientAsync(ServiceClientAsync):
    def __init__(self, config: BotFrameworkConnectorConfiguration) -> None:
        super(ServiceClientAsync, self).__init__(config)

        self.config.pipeline = config.pipeline or self._create_default_pipeline()
