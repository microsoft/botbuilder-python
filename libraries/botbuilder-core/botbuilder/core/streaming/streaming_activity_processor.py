# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC
from typing import Awaitable, Callable

from botbuilder.core import TurnContext, InvokeResponse
from botbuilder.schema import Activity


class StreamingActivityProcessor(ABC):
    """
    Process streaming activities.
    """

    async def process_streaming_activity(
        self,
        activity: Activity,
        bot_callback_handler: Callable[[TurnContext], Awaitable],
    ) -> InvokeResponse:
        raise NotImplementedError()
