# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class Claim:
    def __init__(self, claim_type: str, value):
        self.type = claim_type
        self.value = value


class ClaimsIdentity:
    def __init__(
        self, claims: dict, is_authenticated: bool, authentication_type: str = None
    ):
        self.claims = claims
        self.is_authenticated = is_authenticated
        self.authentication_type = authentication_type

    def get_claim_value(self, claim_type: str):
        return self.claims.get(claim_type)
