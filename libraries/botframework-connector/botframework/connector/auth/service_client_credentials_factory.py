# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

from .app_credentials import AppCredentials


class ServiceClientCredentialsFactory(ABC):
    @abstractmethod
    async def is_valid_app_id(self, app_id: str) -> bool:
        """
        Validates an app ID.

        :param app_id: The app ID to validate.
        :returns: The result is true if `app_id` is valid for the controller; otherwise, false.
        """
        raise NotImplementedError()

    @abstractmethod
    async def is_authentication_disabled(self) -> bool:
        """
        Checks whether bot authentication is disabled.

        :returns: If bot authentication is disabled, the result is true; otherwise, false.
        """
        raise NotImplementedError()

    @abstractmethod
    async def create_credentials(
        self,
        app_id: str,
        oauth_scope: str,
        login_endpoint: str,
        validate_authority: bool,
    ) -> AppCredentials:
        """
        A factory method for creating AppCredentials.

        :param app_id: The appId.
        :param audience: The audience.
        :param login_endpoint: The login url.
        :param validate_authority: The validate authority value to use.
        :returns: An AppCredentials object.
        """
        raise NotImplementedError()
