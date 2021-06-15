# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from asyncio import Future, shield
from uuid import UUID
from typing import Dict

import botframework.streaming as streaming


class RequestManager:
    def __init__(
        self,
        *,
        pending_requests: Dict[UUID, "Future[streaming.ReceiveResponse]"] = None
    ):
        self._pending_requests = pending_requests or {}

    async def signal_response(
        self, request_id: UUID, response: "streaming.ReceiveResponse"
    ) -> bool:
        # TODO: dive more into this logic
        signal: Future = self._pending_requests.get(request_id)
        if signal:
            signal.set_result(response)
            # TODO: double check this
            # del self._pending_requests[request_id]

            return True

        return False

    async def get_response(self, request_id: UUID) -> "streaming.ReceiveResponse":
        if request_id in self._pending_requests:
            return None

        pending_request = Future()
        self._pending_requests[request_id] = pending_request

        try:
            response: streaming.ReceiveResponse = await shield(pending_request)
            return response

        finally:
            del self._pending_requests[request_id]
