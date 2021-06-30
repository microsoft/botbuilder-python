# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

from botbuilder.schema import Activity, CallerIdConstants

from botframework.connector.skills import BotFrameworkClient

from .authenticate_request_result import AuthenticateRequestResult
from .claims_identity import ClaimsIdentity
from .connector_factory import ConnectorFactory
from .jwt_token_validation import JwtTokenValidation
from .user_token_client import UserTokenClient
from .service_client_credentials_factory import ServiceClientCredentialsFactory
from .skill_validation import SkillValidation


class BotFrameworkAuthentication(ABC):
    @abstractmethod
    async def authenticate_request(
        self, activity: Activity, auth_header: str
    ) -> AuthenticateRequestResult:
        """
        Validate Bot Framework Protocol requests.

        :param activity: The inbound Activity.
        :param auth_header: The HTTP auth header.
        :return: An AuthenticateRequestResult.
        """
        raise NotImplementedError()

    @abstractmethod
    async def authenticate_streaming_request(
        self, auth_header: str, channel_id_header: str
    ) -> AuthenticateRequestResult:
        """
        Validate Bot Framework Protocol requests.

        :param auth_header: The HTTP auth header.
        :param channel_id_header: The channel ID HTTP header.
        :return: An AuthenticateRequestResult.
        """
        raise NotImplementedError()

    @abstractmethod
    def create_connector_factory(
        self, claims_identity: ClaimsIdentity
    ) -> ConnectorFactory:
        """
        Creates a ConnectorFactory that can be used to create ConnectorClients that can use credentials
        from this particular Cloud Environment.

        :param claims_identity: The inbound Activity's ClaimsIdentity.
        :return: A ConnectorFactory.
        """
        raise NotImplementedError()

    @abstractmethod
    async def create_user_token_client(
        self, claims_identity: ClaimsIdentity
    ) -> UserTokenClient:
        """
        Creates the appropriate UserTokenClient instance.

        :param claims_identity: The inbound Activity's ClaimsIdentity.
        :return: An UserTokenClient.
        """
        raise NotImplementedError()

    def create_bot_framework_client(self) -> BotFrameworkClient:
        """
        Creates a BotFrameworkClient for calling Skills.

        :return: A BotFrameworkClient.
        """
        raise Exception("NotImplemented")

    def get_originating_audience(self) -> str:
        """
        Gets the originating audience from Bot OAuth scope.

        :return: The originating audience.
        """
        raise Exception("NotImplemented")

    async def authenticate_channel_request(self, auth_header: str) -> ClaimsIdentity:
        """
        Authenticate Bot Framework Protocol request to Skills.

        :param auth_header: The HTTP auth header in the skill request.
        :return: A ClaimsIdentity.
        """
        raise Exception("NotImplemented")

    async def generate_caller_id(
        self,
        *,
        credential_factory: ServiceClientCredentialsFactory,
        claims_identity: ClaimsIdentity,
        caller_id: str,
    ) -> str:
        """
        Generates the appropriate caller_id to write onto the Activity, this might be None.

        :param credential_factory A ServiceClientCredentialsFactory to use.
        :param claims_identity The inbound claims.
        :param caller_id The default caller_id to use if this is not a skill.
        :return: The caller_id, this might be None.
        """
        # Is the bot accepting all incoming messages?
        if await credential_factory.is_authentication_disabled():
            # Return None so that the caller_id is cleared.
            return None

        # Is the activity from another bot?
        return (
            f"{CallerIdConstants.bot_to_bot_prefix}{JwtTokenValidation.get_app_id_from_claims(claims_identity.claims)}"
            if SkillValidation.is_skill_claim(claims_identity.claims)
            else caller_id
        )
