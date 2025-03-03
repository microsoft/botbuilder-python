# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Union

class DateTimeResolution:
    def __init__(
        self, value: Union[str, None] = None, start: Union[str, None] = None, end: Union[str, None] = None, timex: Union[str, None] = None
    ):
        self.value = value
        self.start = start
        self.end = end
        self.timex = timex
