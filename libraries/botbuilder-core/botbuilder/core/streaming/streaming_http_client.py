# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from http import HTTPStatus
from logging import Logger

from botbuilder.streaming import StreamingRequest

from .streaming_request_handler import StreamingRequestHandler


class StreamingHttpClient:
    def __init__(self, request_handler: StreamingRequestHandler, logger: Logger = None):
        if not request_handler:
            raise TypeError(f"'request_handler: {request_handler.__class__.__name__}' argument can't be None")
        self._request_handler = request_handler
        self._logger = logger
    
    async def send(self, request: object) -> object:
        # TODO: validate form of request to perform operations
        streaming_request = StreamingRequest(
            path=request.path[request.path.index("/v3"):],
            verb=request.method
        )
        streaming_request.set_body(request.content)

        return await self._send_request(streaming_request)

    async def _send_request(self, request: StreamingRequest) -> object:
        try:
            server_response = await self._request_handler.send_streaming_request(request)

            if not server_response:
                raise Exception("Server response from streaming request is None")

            if server_response.status_code == HTTPStatus.OK:
                # TODO: this should be an object read from json
                return server_response.read_body_as_str()
        except Exception as error:
            # TODO: log error
            pass

        return None
