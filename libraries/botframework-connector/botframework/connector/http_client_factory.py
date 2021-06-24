# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .http_client_base import HttpClientBase


class HttpClientFactory:
    def create_client(self) -> HttpClientBase:
        pass
