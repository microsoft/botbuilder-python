# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import platform

from aiohttp import ClientResponse, ClientSession, ClientTimeout

from ... import __title__, __version__

from ..qnamaker_endpoint import QnAMakerEndpoint


class HttpRequestUtils:
    """ HTTP request utils class. """

    def __init__(self, http_client: ClientSession):
        self._http_client = http_client

    async def execute_http_request(
        self,
        request_url: str,
        payload_body: object,
        endpoint: QnAMakerEndpoint,
        timeout: float = None,
    ) -> ClientResponse:
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

        if timeout:
            # Convert miliseconds to seconds (as other BotBuilder SDKs accept timeout value in miliseconds)
            # aiohttp.ClientSession units are in seconds
            request_timeout = ClientTimeout(total=timeout / 1000)

            response: ClientResponse = await self._http_client.post(
                request_url,
                data=serialized_payload_body,
                headers=headers,
                timeout=request_timeout,
            )
        else:
            response: ClientResponse = await self._http_client.post(
                request_url, data=serialized_payload_body, headers=headers
            )

        return response

    def _get_headers(self, endpoint: QnAMakerEndpoint):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": self._get_user_agent(),
            "Authorization": f"EndpointKey {endpoint.endpoint_key}",
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
