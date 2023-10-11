# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from msrest.service_client import SDKClient
from msrest import Serializer, Deserializer

from ._configuration import ConnectorClientConfiguration
from .operations import AttachmentsOperations
from .operations import ConversationsOperations
from . import models


class ConnectorClient(SDKClient):
    """The Bot Connector REST API allows your bot to send and receive messages to channels configured in the
    [Bot Framework Developer Portal](https://dev.botframework.com). The Connector service uses industry-standard REST
    and JSON over HTTPS.
    Client libraries for this REST API are available. See below for a list.
    Many bots will use both the Bot Connector REST API and the associated [Bot State REST API](/en-us/restapi/state).
    The Bot State REST API allows a bot to store and retrieve state associated with users and conversations.
    Authentication for both the Bot Connector and Bot State REST APIs is accomplished with JWT Bearer tokens, and is
    described in detail in the [Connector Authentication](/en-us/restapi/authentication) document.
    # Client Libraries for the Bot Connector REST API
    * [Bot Builder for C#](/en-us/csharp/builder/sdkreference/)
    * [Bot Builder for Node.js](/en-us/node/builder/overview/)
    * Generate your own from the
    [Connector API Swagger file](https://raw.githubusercontent.com/Microsoft/BotBuilder/master/CSharp/Library
    /Microsoft.Bot.Connector.Shared/Swagger/ConnectorAPI.json)
    © 2016 Microsoft

    :ivar config: Configuration for client.
    :vartype config: ConnectorClientConfiguration

    :ivar attachments: Attachments operations
    :vartype attachments: botframework.connector.operations.AttachmentsOperations
    :ivar conversations: Conversations operations
    :vartype conversations: botframework.connector.operations.ConversationsOperations

    :param credentials: Subscription credentials which uniquely identify
     client subscription.
    :type credentials: None
    :param str base_url: Service URL
    """

    def __init__(self, credentials, base_url=None):
        self.config = ConnectorClientConfiguration(credentials, base_url)
        super(ConnectorClient, self).__init__(self.config.credentials, self.config)

        client_models = {
            k: v for k, v in models.__dict__.items() if isinstance(v, type)
        }
        self.api_version = "v3"
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        self.attachments = AttachmentsOperations(
            self._client, self.config, self._serialize, self._deserialize
        )
        self.conversations = ConversationsOperations(
            self._client, self.config, self._serialize, self._deserialize
        )
