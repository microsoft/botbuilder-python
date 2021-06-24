# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .claims_identity import ClaimsIdentity
from .connector_factory import ConnectorFactory


class AuthenticateRequestResult:
    def __init__(self) -> None:
        # A value for the Audience.
        self.audience: str = None
        # A value for the ClaimsIdentity.
        self.claims_identity: ClaimsIdentity = None
        # A value for the caller id.
        self.caller_id: str = None
        # A value for the ConnectorFactory.
        self.connector_factory: ConnectorFactory = None
