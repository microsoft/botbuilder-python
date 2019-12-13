# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datetime import timedelta
from typing import List, Union


class VerifyOptions:
    def __init__(self, issuer, audience, clock_tolerance, ignore_expiration):
        self.issuer: Union[List[str], str] = issuer or []
        self.audience: str = audience
        self.clock_tolerance: Union[int, timedelta] = clock_tolerance or 0
        self.ignore_expiration: bool = ignore_expiration or False
