# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.core import Bot, BotFrameworkAdapter, BotFrameworkAdapterSettings
from botframework.connector.auth import ClaimsIdentity

from .streaming_activity_processor import StreamingActivityProcessor


class BotFrameworkHttpAdapterBase(BotFrameworkAdapter, StreamingActivityProcessor):
    def __init__(self, settings: BotFrameworkAdapterSettings):
        super().__init__(self, settings)

        self._connected_bot: Bot = None
        self._claims_identity: ClaimsIdentity = None
        self._request_handlers: List[object] = None
