# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import platform
from typing import Any
import requests

from aiohttp import ClientResponse, ClientSession, ClientTimeout

from ... import __title__, __version__

from ..qnamaker_endpoint import QnAMakerEndpoint


class HttpRequestUtils:
    """HTTP request utils class.

    Parameters:
    -----------

    http_client: Client to make HTTP requests with. Default client used in the SDK is `aiohttp.ClientSession`.
    """

    def __init__(self, http_client: Any):
        self._http_client = http_client

    async def execute_http_request(
        self,
        request_url: str,
        payload_body: object,
        endpoint: QnAMakerEndpoint,
        timeout: float = None,
    ) -> Any:
        """
        Execute HTTP request.

        Parameters:
        -----------

        request_url: HTTP request URL.

        payload_body: HTTP request body.

        endpoint: QnA Maker endpoint details.

        timeout: Timeout for HTTP call (milliseconds).
        """
        if not request_url:
            raise TypeError(
                "HttpRequestUtils.execute_http_request(): request_url cannot be None."
            )

        if not payload_body:
            raise TypeError(
                "HttpRequestUtils.execute_http_request(): question cannot be None."
            )

        if not endpoint:
            raise TypeError(
                "HttpRequestUtils.execute_http_request(): endpoint cannot be None."
            )

        serialized_payload_body = json.dumps(payload_body.serialize())

        headers = self._get_headers(endpoint)

        if isinstance(self._http_client, ClientSession):
            response: ClientResponse = await self._make_request_with_aiohttp(
                request_url, serialized_payload_body, headers, timeout
            )
        elif self._is_using_requests_module():
            response: requests.Response = self._make_request_with_requests(
                request_url, serialized_payload_body, headers, timeout
            )
        else:
            response = await self._http_client.post(
                request_url, data=serialized_payload_body, headers=headers
            )

        return response

    def _get_headers(self, endpoint: QnAMakerEndpoint):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": self._get_user_agent(),
            "Authorization": f"EndpointKey {endpoint.endpoint_key}",
            "Ocp-Apim-Subscription-Key": f"EndpointKey {endpoint.endpoint_key}",
        }

        return headers

    def _get_user_agent(self):
        package_user_agent = f"{__title__}/{__version__}"
        uname = platform.uname()
        os_version = f"{uname.machine}-{uname.system}-{uname.version}"
        py_version = f"Python,Version={platform.python_version()}"
        platform_user_agent = f"({os_version}; {py_version})"
        user_agent = f"{package_user_agent} {platform_user_agent}"

        return user_agent

    def _is_using_requests_module(self) -> bool:
        return (type(self._http_client).__name__ == "module") and (
            self._http_client.__name__ == "requests"
        )

    async def _make_request_with_aiohttp(
        self, request_url: str, payload_body: str, headers: dict, timeout: float
    ) -> ClientResponse:
        if timeout:
            # aiohttp.ClientSession's timeouts are in seconds
            timeout_in_seconds = ClientTimeout(total=timeout / 1000)

            return await self._http_client.post(
                request_url,
                data=payload_body,
                headers=headers,
                timeout=timeout_in_seconds,
            )

        return await self._http_client.post(
            request_url, data=payload_body, headers=headers
        )

    def _make_request_with_requests(
        self, request_url: str, payload_body: str, headers: dict, timeout: float
    ) -> requests.Response:
        if timeout:
            # requests' timeouts are in seconds
            timeout_in_seconds = timeout / 1000

            return self._http_client.post(
                request_url,
                data=payload_body,
                headers=headers,
                timeout=timeout_in_seconds,
            )

        return self._http_client.post(request_url, data=payload_body, headers=headers)
