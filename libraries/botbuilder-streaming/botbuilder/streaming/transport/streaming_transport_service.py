# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC


class StreamingTransportService(ABC):
    async def start(self):
        raise NotImplementedError()

    async def send(self, request):
        raise NotImplementedError()
