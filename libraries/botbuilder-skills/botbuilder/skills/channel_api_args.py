# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List


class ChannelApiArgs:
    def __init__(
        self,
        method: str = None,
        args: List[object] = None,
        result: object = None,
        exception: Exception = None,
    ):
        self.method = method
        self.args = args
        self.result = result
        self.exception = exception
