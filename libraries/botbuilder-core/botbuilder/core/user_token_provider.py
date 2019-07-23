# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from typing import Dict, List

from botbuilder.schema import TokenResponse

from .turn_context import TurnContext


class UserTokenProvider(ABC):
    @abstractmethod
    async def get_user_token(
        self, context: TurnContext, connection_name: str, magic_code: str = None
    ) -> TokenResponse:
        """
        Retrieves the OAuth token for a user that is in a sign-in flow.
        :param context:
        :param connection_name:
        :param magic_code:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def sign_out_user(
        self, context: TurnContext, connection_name: str, user_id: str = None
    ):
        """
        Signs the user out with the token server.
        :param context:
        :param connection_name:
        :param user_id:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_oauth_sign_in_link(
        self, context: TurnContext, connection_name: str
    ) -> str:
        """
        Get the raw signin link to be sent to the user for signin for a connection name.
        :param context:
        :param connection_name:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_aad_tokens(
        self, context: TurnContext, connection_name: str, resource_urls: List[str]
    ) -> Dict[str, TokenResponse]:
        """
        Retrieves Azure Active Directory tokens for particular resources on a configured connection.
        :param context:
        :param connection_name:
        :param resource_urls:
        :return:
        """
        raise NotImplementedError()
