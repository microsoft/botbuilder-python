# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from aiohttp import ClientSession, ClientResponse, ClientResponseError

from botframework.connector import (
    HttpClientBase,
    HttpClientFactory,
    HttpRequest,
    HttpResponseBase,
)


class _HttpResponseImpl(HttpResponseBase):
    def __init__(self, client_response: ClientResponse) -> None:
        self._client_response = client_response

    @property
    def status_code(self):
        return self._client_response.status

    async def is_succesful(self) -> bool:
        try:
            self._client_response.raise_for_status()
            return True
        except ClientResponseError:
            return False

    async def read_content_str(self) -> str:
        return (await self._client_response.read()).decode()


class _HttpClientImplementation(HttpClientBase):
    async def post(self, *, request: HttpRequest) -> HttpResponseBase:
        async with ClientSession() as session:
            aio_response = await session.post(
                request.request_uri, data=request.content, headers=request.headers
            )

        return _HttpResponseImpl(aio_response)


class AioHttpClientFactory(HttpClientFactory):
    def create_client(self) -> HttpClientBase:
        return _HttpClientImplementation()
