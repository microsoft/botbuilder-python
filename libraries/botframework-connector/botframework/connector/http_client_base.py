# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

from .http_request import HttpRequest
from .http_response_base import HttpResponseBase


class HttpClientBase(ABC):
    @abstractmethod
    async def post(self, *, request: HttpRequest) -> HttpResponseBase:
        raise NotImplementedError()
