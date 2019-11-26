# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .channel_provider import ChannelProvider
from .government_constants import GovernmentConstants


class SimpleChannelProvider(ChannelProvider):
    """
    ChannelProvider interface. This interface allows Bots to provide their own
    implementation for the configuration parameters to connect to a Bot.
    Framework channel service.
    """

    def __init__(self, channel_service: str = None):
        self.channel_service = channel_service

    async def get_channel_service(self) -> str:
        return self.channel_service

    def is_government(self) -> bool:
        return self.channel_service == GovernmentConstants.CHANNEL_SERVICE

    def is_public_azure(self) -> bool:
        return not self.channel_service
