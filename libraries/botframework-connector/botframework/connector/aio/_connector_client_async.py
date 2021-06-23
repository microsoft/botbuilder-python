# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from typing import Optional, Type

from msrest.universal_http.async_abc import AsyncHTTPSender as AsyncHttpDriver
from msrest.pipeline.aiohttp import AsyncHTTPSender
from msrest.async_client import AsyncPipeline
from msrest import Serializer, Deserializer

from .operations_async import AttachmentsOperations
from .operations_async import ConversationsOperations
from .. import models


from ..bot_framework_sdk_client_async import (
    BotFrameworkSDKClientAsync,
    BotFrameworkConnectorConfiguration,
)


class ConnectorClient(BotFrameworkSDKClientAsync):
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
    [Connector API Swagger file](https://raw.githubusercontent.com/Microsoft/BotBuilder/master/CSharp/Library/
    Microsoft.Bot.Connector.Shared/Swagger/ConnectorAPI.json)
    © 2016 Microsoft

    :ivar config: Configuration for client.
    :vartype config: ConnectorClientConfiguration

    :ivar attachments: Attachments operations
    :vartype attachments: botframework.connector.aio.operations_async.AttachmentsOperations
    :ivar conversations: Conversations operations
    :vartype conversations: botframework.connector.aio.operations_async.ConversationsOperations

    :param credentials: Subscription credentials which uniquely identify
     client subscription.
    :type credentials: None
    :param str base_url: Service URL
    """

    def __init__(
        self,
        credentials,
        base_url=None,
        *,
        pipeline_type: Optional[Type[AsyncPipeline]] = None,
        sender: Optional[AsyncHTTPSender] = None,
        driver: Optional[AsyncHttpDriver] = None,
        custom_configuration: Optional[BotFrameworkConnectorConfiguration] = None,
    ):
        if custom_configuration:
            self.config = custom_configuration
        else:
            self.config = BotFrameworkConnectorConfiguration(
                credentials,
                base_url,
                pipeline_type=pipeline_type,
                sender=sender,
                driver=driver,
            )
        super(ConnectorClient, self).__init__(self.config)

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
