# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json, platform, requests
from aiohttp import ClientSession, ClientTimeout
from typing import Union
#TODO fix importing title and version
# from ../.. import __title__, __version__ 

from ..qnamaker_endpoint import QnAMakerEndpoint

class HttpRequestUtils:
    """ HTTP request utils class. """

    def __init__(self, http_client: Union[ClientSession, object]):
        self._http_client = http_client

    #TODO figure out return type
    async def execute_http_request(
        self,
        request_url: str,
        #TODO verify if this is str in python
        payload_body: str,
        endpoint: QnAMakerEndpoint,
        timeout: float=None
    ):
        """
        Execute HTTP request.

        Parameters:
        -----------

        request_url: HTTP request URL.

        payload_body: HTTP request body.

        endpoint: QnA Maker endpoint details.

        timeout: (Optional) Timeout for HTTP call.
        """
        if not request_url:
            raise TypeError("HttpRequestUtils.execute_http_request(): request_url cannot be None.")
        
        if not payload_body:
            raise TypeError("HttpRequestUtils.execute_http_request(): payload_body cannot be None.")
        
        if  not endpoint:
            raise TypeError("HttpRequestUtils.execute_http_request(): endpoint cannot be None.")
        
        headers = self._get_headers(endpoint)

        # Convert miliseconds to seconds (as other BotBuilder SDKs accept timeout value in miliseconds)
        # aiohttp.ClientSession units are in seconds
        timeout = ClientTimeout(total=timeout / 1000)

        #TODO figure out at what point you want to serialize payload_body
        response = await self._http_client.post(
            request_url, data=payload_body, headers=headers, timeout=timeout
        )

        return response
    
    def _get_headers(self, endpoint: QnAMakerEndpoint):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": self._get_user_agent(),
        }

        if endpoint.host.endswith("v3.0"):
            headers["Ocp-Apim-Subscription-Key"] = endpoint.endpoint_key
        else:
            headers["Authorization"] = f"EndpointKey {endpoint.endpoint_key}"

        return headers

    def _get_user_agent(self):
        # package_user_agent = f"{__title__}/{__version__}"
        uname = platform.uname()
        os_version = f"{uname.machine}-{uname.system}-{uname.version}"
        py_version = f"Python,Version={platform.python_version()}"
        f"({os_version}; {py_version})"
        # TODO delete above line, and use platform_user_agent variable
        # platform_user_agent = f"({os_version}; {py_version})"
        # user_agent = f"{package_user_agent} {platform_user_agent}"
        user_agent = "CHANGE THIS LATER"

        return user_agent