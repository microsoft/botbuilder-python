# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from msrest.service_client import SDKClient
from msrest import Configuration, Serializer, Deserializer
from .. import models
from .version import VERSION
from .operations.teams_operations import TeamsOperations


class TeamsConnectorClientConfiguration(Configuration):
    """Configuration for TeamsConnectorClient
    Note that all parameters used to create this instance are saved as instance
    attributes.

    :param credentials: Subscription credentials which uniquely identify
     client subscription.
    :type credentials: None
    :param str base_url: Service URL
    """

    def __init__(self, credentials, base_url=None):
        if credentials is None:
            raise ValueError("Parameter 'credentials' must not be None.")
        if not base_url:
            base_url = "https://api.botframework.com"

        super(TeamsConnectorClientConfiguration, self).__init__(base_url)

        self.add_user_agent("botframework-connector/{}".format(VERSION))

        self.credentials = credentials


class TeamsConnectorClient(SDKClient):
    """﻿﻿The Bot Connector REST API extension for Microsoft Teams allows your bot to perform extended
    operations on to Microsoft Teams channel configured in the
    [Bot Framework Developer Portal](https://dev.botframework.com). The Connector service uses
    industry-standard REST and JSON over HTTPS. Client libraries for this REST API are available. See below for a list.
    Authentication for both the Bot Connector and Bot State REST APIs is accomplished with JWT Bearer tokens, and is
    described in detail in the [Connector Authentication](https://docs.botframework.com/en-us/restapi/authentication)
     document.
    # Client Libraries for the Bot Connector REST API
    * [Bot Builder for C#](https://docs.botframework.com/en-us/csharp/builder/sdkreference/)
    * [Bot Builder for Node.js](https://docs.botframework.com/en-us/node/builder/overview/)
    © 2016 Microsoft

    :ivar config: Configuration for client.
    :vartype config: TeamsConnectorClientConfiguration

    :ivar teams: Teams operations
    :vartype teams: botframework.connector.teams.operations.TeamsOperations

    :param credentials: Subscription credentials which uniquely identify
     client subscription.
    :type credentials: None
    :param str base_url: Service URL
    """

    def __init__(self, credentials, base_url=None):
        self.config = TeamsConnectorClientConfiguration(credentials, base_url)
        super(TeamsConnectorClient, self).__init__(self.config.credentials, self.config)

        client_models = {
            k: v for k, v in models.__dict__.items() if isinstance(v, type)
        }
        self.api_version = "v3"
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        self.teams = TeamsOperations(
            self._client, self.config, self._serialize, self._deserialize
        )
