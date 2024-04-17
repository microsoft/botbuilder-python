# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Awaitable, Callable, Dict, List

from .authentication_constants import AuthenticationConstants


class AuthenticationConfiguration:
    def __init__(
        self,
        required_endorsements: List[str] = None,
        claims_validator: Callable[[List[Dict]], Awaitable] = None,
        valid_token_issuers: List[str] = None,
        tenant_id: str = None,
    ):
        self.required_endorsements = required_endorsements or []
        self.claims_validator = claims_validator
        self.valid_token_issuers = valid_token_issuers or []

        if tenant_id:
            self.add_tenant_issuers(self, tenant_id)

    @staticmethod
    def add_tenant_issuers(authentication_configuration, tenant_id: str):
        authentication_configuration.valid_token_issuers.append(
            AuthenticationConstants.VALID_TOKEN_ISSUER_URL_TEMPLATE_V1.format(tenant_id)
        )
        authentication_configuration.valid_token_issuers.append(
            AuthenticationConstants.VALID_TOKEN_ISSUER_URL_TEMPLATE_V2.format(tenant_id)
        )
        authentication_configuration.valid_token_issuers.append(
            AuthenticationConstants.VALID_GOVERNMENT_TOKEN_ISSUER_URL_TEMPLATE_V1.format(
                tenant_id
            )
        )
        authentication_configuration.valid_token_issuers.append(
            AuthenticationConstants.VALID_GOVERNMENT_TOKEN_ISSUER_URL_TEMPLATE_V2.format(
                tenant_id
            )
        )
