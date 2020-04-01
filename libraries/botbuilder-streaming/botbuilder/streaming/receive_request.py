# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List


class ReceiveRequest:
    def __init__(self, *, verb: str = None, path: str = None, streams: List[object]):
        self.verb = verb
        self.path = path
        self.streams = streams or []
