# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod


class ChannelProvider(ABC):
    """
    ChannelProvider interface. This interface allows Bots to provide their own
    implementation for the configuration parameters to connect to a Bot.
    Framework channel service.
    """

    @abstractmethod
    async def get_channel_service(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def is_government(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_public_azure(self) -> bool:
        raise NotImplementedError()
