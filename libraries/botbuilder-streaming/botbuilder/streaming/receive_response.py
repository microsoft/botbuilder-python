# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.streaming.payloads import ContentStream


class ReceiveResponse:
    def __init__(self, status_code: int = None, streams: List[ContentStream] = None):
        self.status_code = status_code
        self.streams = streams
