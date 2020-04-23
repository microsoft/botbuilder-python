# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from http import HTTPStatus
from logging import Logger
from typing import Any, Optional

from msrest.universal_http import ClientRequest
from msrest.universal_http.async_abc import AsyncClientResponse, AsyncHTTPSender
from botbuilder.streaming import StreamingRequest, ReceiveResponse

from .streaming_request_handler import StreamingRequestHandler


class StreamingProtocolClientResponse(AsyncClientResponse):
    def __init__(
        self, request: StreamingRequest, streaming_response: ReceiveResponse
    ) -> None:
        super(StreamingProtocolClientResponse, self).__init__(
            request, streaming_response
        )
        # https://aiohttp.readthedocs.io/en/stable/client_reference.html#aiohttp.ClientResponse
        self.status_code = streaming_response.status_code
        # self.headers = streaming_response.headers
        # self.reason = streaming_response.reason
        self._body = None

    def body(self) -> bytes:
        """Return the whole body as bytes in memory.
        """
        if not self._body:
            raise ValueError(
                "Body is not available. Call async method load_body, or do your call with stream=False."
            )
        return self._body

    async def load_body(self) -> None:
        """Load in memory the body, so it could be accessible from sync methods."""
        self._body: ReceiveResponse
        self._body = self.internal_response.read_body()

    def raise_for_status(self):
        if 400 <= self.internal_response.status_code <= 599:
            raise Exception(f"Http error: {self.internal_response.status_code}")


class StreamingHttpDriver(AsyncHTTPSender):
    def __init__(self, request_handler: StreamingRequestHandler, logger: Logger = None):
        if not request_handler:
            raise TypeError(
                f"'request_handler: {request_handler.__class__.__name__}' argument can't be None"
            )
        self._request_handler = request_handler
        self._logger = logger

    async def __aenter__(self):
        raise Exception("This driver currently does not support context manager")

    async def __aexit__(self, *exc_details):  # pylint: disable=arguments-differ
        raise Exception("This driver currently does not support context manager")

    async def send(self, request: ClientRequest, **config: Any) -> AsyncClientResponse:
        # TODO: validate form of request to perform operations
        streaming_request = StreamingRequest(
            path=request.url[request.url.index("/v3") :], verb=request.method
        )
        streaming_request.set_body(request.data)

        return await self._send_request(streaming_request)

    async def _send_request(
        self, request: StreamingRequest
    ) -> StreamingProtocolClientResponse:
        try:
            server_response = await self._request_handler.send_streaming_request(
                request
            )

            if not server_response:
                raise Exception("Server response from streaming request is None")

            if server_response.status_code == HTTPStatus.OK:
                # TODO: this should be an object read from json

                return StreamingProtocolClientResponse(request, server_response)
        except Exception as error:
            # TODO: log error
            raise error
            pass

        return None
