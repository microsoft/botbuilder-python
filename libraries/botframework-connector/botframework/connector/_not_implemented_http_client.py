# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .http_client_base import HttpClientBase
from .http_request import HttpRequest
from .http_response_base import HttpResponseBase


class _NotImplementedHttpClient(HttpClientBase):
    async def post(
        self, *, request: HttpRequest  # pylint: disable=unused-argument
    ) -> HttpResponseBase:
        raise RuntimeError(
            "Please provide an http implementation for the skill BotFrameworkClient"
        )
