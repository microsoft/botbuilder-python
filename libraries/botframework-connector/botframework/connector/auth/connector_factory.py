# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

from botframework.connector.aio import ConnectorClient


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
