# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Any

from botframework.connector.auth import PasswordServiceClientCredentialFactory


class ConfigurationServiceClientCredentialFactory(
    PasswordServiceClientCredentialFactory
):
    def __init__(self, configuration: Any) -> None:
        if not hasattr(configuration, "APP_ID"):
            raise Exception("Property 'APP_ID' is expected in configuration object")
        if not hasattr(configuration, "APP_PASSWORD"):
            raise Exception(
                "Property 'APP_PASSWORD' is expected in configuration object"
            )
        super().__init__(configuration.APP_ID, configuration.APP_PASSWORD)
