# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from asyncio import Future
from uuid import UUID
from typing import Dict

from botbuilder.streaming import ReceiveResponse


class RequestManager:
    def __init__(self, *, pending_requests: Dict[UUID, "Future[ReceiveResponse]"]):
        self._pending_requests = pending_requests or {}

    def signal_response(
        self, request_id: UUID, response: "Future[ReceiveResponse]"
    ) -> bool:
        # TODO: dive more into this logic
        signal: Future = self._pending_requests.get(request_id)
        if signal:
            signal.set_result(response)
            # TODO: double check this
            del self._pending_requests[request_id]

            return True

        return False

    async def get_response(self, request_id: UUID) -> ReceiveResponse:
        if request_id in self._pending_requests:
            return None

        pending_request = Future()
        self._pending_requests[request_id] = pending_request

        try:
            response: ReceiveResponse = await pending_request
            return response

        finally:
            del self._pending_requests[request_id]
