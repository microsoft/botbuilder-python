# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC

from .transport_base import TransportBase


class TransportSenderBase(ABC, TransportBase):
    async def send(self, buffer: object, offset: int, count: int) -> int:
        raise NotImplementedError()
