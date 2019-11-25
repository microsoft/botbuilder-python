# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List


class AuthenticationConfiguration:
    def __init__(self, required_endorsements: List[str] = None):
        self.required_endorsements = required_endorsements or []
