# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .connector_factory import ConnectorFactory
from .service_client_credentials_factory import ServiceClientCredentialsFactory


class ConnectorFactoryImpl(ConnectorFactory):
    def __init__(self, app_id: str, to_channel_from_bot_oauth_scope: str, login_enpoint: str, validate_authority: bool, credential_factory: ServiceClientCredentialsFactory) -> None:
        self._app_id = app_id
        self._to_channel_from_bot_oauth_scope = to_channel_from_bot_oauth_scope
        self._login_enpoint = login_enpoint
        self._validate_authority = validate_authority
        self._credential_factory = credential_factory