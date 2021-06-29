# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botframework.connector.auth import BotFrameworkAuthentication, ClaimsIdentity

from .channel_service_handler import ChannelServiceHandler


class CloudChannelServiceHandler(ChannelServiceHandler):
    def __init__(  # pylint: disable=super-init-not-called
        self, auth: BotFrameworkAuthentication
    ):
        if not auth:
            raise TypeError("Auth can't be None")
        self._auth = auth

    async def _authenticate(self, auth_header: str) -> ClaimsIdentity:
        return await self._auth.authenticate_channel_request(auth_header)
