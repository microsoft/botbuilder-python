# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger
from typing import Any

from botframework.connector.auth import PasswordServiceClientCredentialFactory


class ConfigurationServiceClientCredentialFactory(
    PasswordServiceClientCredentialFactory
):
    def __init__(self, configuration: Any, *, logger: Logger = None) -> None:
        super().__init__(
            app_id=getattr(configuration, "APP_ID", None),
            password=getattr(configuration, "APP_PASSWORD", None),
            logger=logger,
        )
