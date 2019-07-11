# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class DateTimeResolution:
    def __init__(
        self, value: str = None, start: str = None, end: str = None, timex: str = None
    ):
        self.value = value
        self.start = start
        self.end = end
        self.timex = timex
