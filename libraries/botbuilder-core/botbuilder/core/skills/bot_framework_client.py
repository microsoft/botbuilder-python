# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC

from botbuilder.schema import Activity
from botbuilder.core import InvokeResponse


class BotFrameworkClient(ABC):
    def post_activity(
        self,
        from_bot_id: str,
        to_bot_id: str,
        to_url: str,
        service_url: str,
        conversation_id: str,
        activity: Activity,
    ) -> InvokeResponse:
        raise NotImplementedError()
