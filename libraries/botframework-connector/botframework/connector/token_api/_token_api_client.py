# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from msrest.service_client import SDKClient
from msrest import Serializer, Deserializer

from ._configuration import TokenApiClientConfiguration
from .operations._bot_sign_in_operations import BotSignInOperations
from .operations._user_token_operations import UserTokenOperations
from . import models


class TokenApiClient(SDKClient):
    """TokenApiClient

    :ivar config: Configuration for client.
    :vartype config: TokenApiClientConfiguration

    :ivar bot_sign_in: BotSignIn operations
    :vartype bot_sign_in: botframework.tokenapi.operations.BotSignInOperations
    :ivar user_token: UserToken operations
    :vartype user_token: botframework.tokenapi.operations.UserTokenOperations

    :param credentials: Subscription credentials which uniquely identify
     client subscription.
    :type credentials: None
    :param str base_url: Service URL
    """

    def __init__(self, credentials, base_url=None):
        self.config = TokenApiClientConfiguration(credentials, base_url)
        super(TokenApiClient, self).__init__(self.config.credentials, self.config)

        client_models = {
            k: v for k, v in models.__dict__.items() if isinstance(v, type)
        }
        self.api_version = "token"
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        self.bot_sign_in = BotSignInOperations(
            self._client, self.config, self._serialize, self._deserialize
        )
        self.user_token = UserTokenOperations(
            self._client, self.config, self._serialize, self._deserialize
        )
