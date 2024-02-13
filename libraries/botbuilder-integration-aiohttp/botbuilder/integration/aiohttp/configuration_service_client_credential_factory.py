# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger
from typing import Any

from botframework.connector.auth import PasswordServiceClientCredentialFactory


class ConfigurationServiceClientCredentialFactory(
    PasswordServiceClientCredentialFactory
):
    def __init__(self, configuration: Any, *, logger: Logger = None) -> None:
        app_type = (
            configuration.APP_TYPE
            if hasattr(configuration, "APP_TYPE")
            else "MultiTenant"
        )
        app_id = configuration.APP_ID if hasattr(configuration, "APP_ID") else None
        app_password = (
            configuration.APP_PASSWORD
            if hasattr(configuration, "APP_PASSWORD")
            else None
        )
        app_tenantid = None

        if app_type == "UserAssignedMsi":
            raise Exception("UserAssignedMsi APP_TYPE is not supported")

        if app_type == "SingleTenant":
            app_tenantid = (
                configuration.APP_TENANTID
                if hasattr(configuration, "APP_TENANTID")
                else None
            )

            if not app_id:
                raise Exception("Property 'APP_ID' is expected in configuration object")
            if not app_password:
                raise Exception(
                    "Property 'APP_PASSWORD' is expected in configuration object"
                )
            if not app_tenantid:
                raise Exception(
                    "Property 'APP_TENANTID' is expected in configuration object"
                )

        super().__init__(app_id, app_password, app_tenantid, logger=logger)
