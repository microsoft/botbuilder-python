# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC
from logging import Logger

from .receive_request import ReceiveRequest
from .streaming_response import StreamingResponse


class RequestHandler(ABC):
    async def process_request(
        self, request: ReceiveRequest, logger: Logger, context: object
    ) -> StreamingResponse:
        raise NotImplementedError()
