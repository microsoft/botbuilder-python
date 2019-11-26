# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Awaitable, Callable, Dict, List


class AuthenticationConfiguration:
    def __init__(
        self,
        required_endorsements: List[str] = None,
        claims_validator: Callable[[List[Dict]], Awaitable] = None,
    ):
        self.required_endorsements = required_endorsements or []
        self.claims_validator = claims_validator
