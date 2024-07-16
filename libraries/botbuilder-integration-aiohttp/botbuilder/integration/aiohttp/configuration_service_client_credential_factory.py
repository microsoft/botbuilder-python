# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from logging import Logger
from typing import Any

from msrest.authentication import Authentication

from botframework.connector.auth import PasswordServiceClientCredentialFactory
from botframework.connector.auth import ManagedIdentityServiceClientCredentialsFactory
from botframework.connector.auth import ServiceClientCredentialsFactory


class ConfigurationServiceClientCredentialFactory(ServiceClientCredentialsFactory):
    def __init__(self, configuration: Any, *, logger: Logger = None) -> None:
        self._inner = None

        app_type = (
            configuration.APP_TYPE
            if hasattr(configuration, "APP_TYPE")
            else "MultiTenant"
        ).lower()

        app_id = configuration.APP_ID if hasattr(configuration, "APP_ID") else None
        app_password = (
            configuration.APP_PASSWORD
            if hasattr(configuration, "APP_PASSWORD")
            else None
        )
        app_tenantid = None

        if app_type == "userassignedmsi":
            if not app_id:
                raise Exception("Property 'APP_ID' is expected in configuration object")

            app_tenantid = (
                configuration.APP_TENANTID
                if hasattr(configuration, "APP_TENANTID")
                else None
            )
            if not app_tenantid:
                raise Exception(
                    "Property 'APP_TENANTID' is expected in configuration object"
                )

            self._inner = ManagedIdentityServiceClientCredentialsFactory(
                app_id, logger=logger
            )

        elif app_type == "singletenant":
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

            self._inner = PasswordServiceClientCredentialFactory(
                app_id, app_password, app_tenantid, logger=logger
            )

        # Default to MultiTenant
        else:
            # Specifically not checking for appId or password to allow auth disabled scenario
            self._inner = PasswordServiceClientCredentialFactory(
                app_id, app_password, None, logger=logger
            )

    async def is_valid_app_id(self, app_id: str) -> bool:
        return await self._inner.is_valid_app_id(app_id)

    async def is_authentication_disabled(self) -> bool:
        return await self._inner.is_authentication_disabled()

    async def create_credentials(
        self,
        app_id: str,
        oauth_scope: str,
        login_endpoint: str,
        validate_authority: bool,
    ) -> Authentication:
        return await self._inner.create_credentials(
            app_id, oauth_scope, login_endpoint, validate_authority
        )
