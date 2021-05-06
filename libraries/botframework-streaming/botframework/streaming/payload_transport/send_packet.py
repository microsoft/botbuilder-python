# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Awaitable, Callable

from botframework.streaming.payloads.models import Header


class SendPacket:
    def __init__(
        self,
        *,
        header: Header,
        payload: object,
        is_length_known: bool,
        sent_callback: Callable[[Header], Awaitable]
    ):
        self.header = header
        self.payload = payload
        self.is_length_known = is_length_known
        self.sent_callback = sent_callback
