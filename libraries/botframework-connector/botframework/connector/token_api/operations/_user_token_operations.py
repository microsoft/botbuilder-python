# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from msrest.pipeline import ClientRawResponse

from .. import models


class UserTokenOperations:
    """UserTokenOperations operations.

    You should not instantiate directly this class, but create a Client instance that will create it for you and attach
    it as attribute.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    :ivar api_version: The API version to use for the request. Constant value: "token".
    """

    models = models

    def __init__(self, client, config, serializer, deserializer):
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer

        self.config = config
        self.api_version = "token"

    def get_token(
        self,
        user_id,
        connection_name,
        channel_id=None,
        code=None,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """

        :param user_id:
        :type user_id: str
        :param connection_name:
        :type connection_name: str
        :param channel_id:
        :type channel_id: str
        :param code:
        :type code: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: TokenResponse or ClientRawResponse if raw=true
        :rtype: ~botframework.tokenapi.models.TokenResponse or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.tokenapi.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get_token.metadata["url"]

        # Construct parameters
        query_parameters = {}
        query_parameters["userId"] = self._serialize.query("user_id", user_id, "str")
        query_parameters["connectionName"] = self._serialize.query(
            "connection_name", connection_name, "str"
        )
        if channel_id is not None:
            query_parameters["channelId"] = self._serialize.query(
                "channel_id", channel_id, "str"
            )
        if code is not None:
            query_parameters["code"] = self._serialize.query("code", code, "str")
        query_parameters["api-version"] = self._serialize.query(
            "self.api_version", self.api_version, "str"
        )

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 404]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("TokenResponse", response)
        if response.status_code == 404:
            deserialized = self._deserialize("TokenResponse", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    get_token.metadata = {"url": "/api/usertoken/GetToken"}

    def get_aad_tokens(
        self,
        user_id,
        connection_name,
        channel_id=None,
        resource_urls=None,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """

        :param user_id:
        :type user_id: str
        :param connection_name:
        :type connection_name: str
        :param channel_id:
        :type channel_id: str
        :param resource_urls:
        :type resource_urls: list[str]
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: dict or ClientRawResponse if raw=true
        :rtype: dict[str, ~botframework.tokenapi.models.TokenResponse] or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.tokenapi.models.ErrorResponseException>`
        """
        aad_resource_urls = models.AadResourceUrls(resource_urls=resource_urls)

        # Construct URL
        url = self.get_aad_tokens.metadata["url"]

        # Construct parameters
        query_parameters = {}
        query_parameters["userId"] = self._serialize.query("user_id", user_id, "str")
        query_parameters["connectionName"] = self._serialize.query(
            "connection_name", connection_name, "str"
        )
        if channel_id is not None:
            query_parameters["channelId"] = self._serialize.query(
                "channel_id", channel_id, "str"
            )
        query_parameters["api-version"] = self._serialize.query(
            "self.api_version", self.api_version, "str"
        )

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        header_parameters["Content-Type"] = "application/json; charset=utf-8"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        body_content = self._serialize.body(aad_resource_urls, "AadResourceUrls")

        # Construct and send request
        request = self._client.post(
            url, query_parameters, header_parameters, body_content
        )
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("{TokenResponse}", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    get_aad_tokens.metadata = {"url": "/api/usertoken/GetAadTokens"}

    def sign_out(
        self,
        user_id,
        connection_name=None,
        channel_id=None,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """

        :param user_id:
        :type user_id: str
        :param connection_name:
        :type connection_name: str
        :param channel_id:
        :type channel_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.tokenapi.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.sign_out.metadata["url"]

        # Construct parameters
        query_parameters = {}
        query_parameters["userId"] = self._serialize.query("user_id", user_id, "str")
        if connection_name is not None:
            query_parameters["connectionName"] = self._serialize.query(
                "connection_name", connection_name, "str"
            )
        if channel_id is not None:
            query_parameters["channelId"] = self._serialize.query(
                "channel_id", channel_id, "str"
            )
        query_parameters["api-version"] = self._serialize.query(
            "self.api_version", self.api_version, "str"
        )

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.delete(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 204]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("object", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    sign_out.metadata = {"url": "/api/usertoken/SignOut"}

    def get_token_status(
        self,
        user_id,
        channel_id=None,
        include=None,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """

        :param user_id:
        :type user_id: str
        :param channel_id:
        :type channel_id: str
        :param include:
        :type include: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: list or ClientRawResponse if raw=true
        :rtype: list[~botframework.tokenapi.models.TokenStatus] or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.tokenapi.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get_token_status.metadata["url"]

        # Construct parameters
        query_parameters = {}
        query_parameters["userId"] = self._serialize.query("user_id", user_id, "str")
        if channel_id is not None:
            query_parameters["channelId"] = self._serialize.query(
                "channel_id", channel_id, "str"
            )
        if include is not None:
            query_parameters["include"] = self._serialize.query(
                "include", include, "str"
            )
        query_parameters["api-version"] = self._serialize.query(
            "self.api_version", self.api_version, "str"
        )

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("[TokenStatus]", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    get_token_status.metadata = {"url": "/api/usertoken/GetTokenStatus"}

    def exchange_async(
        self,
        user_id,
        connection_name,
        channel_id,
        uri=None,
        token=None,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """

        :param user_id:
        :type user_id: str
        :param connection_name:
        :type connection_name: str
        :param channel_id:
        :type channel_id: str
        :param uri:
        :type uri: str
        :param token:
        :type token: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: object or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.tokenapi.models.ErrorResponseException>`
        """
        exchange_request = models.TokenExchangeRequest(uri=uri, token=token)

        # Construct URL
        url = self.exchange_async.metadata["url"]

        # Construct parameters
        query_parameters = {}
        query_parameters["userId"] = self._serialize.query("user_id", user_id, "str")
        query_parameters["connectionName"] = self._serialize.query(
            "connection_name", connection_name, "str"
        )
        query_parameters["channelId"] = self._serialize.query(
            "channel_id", channel_id, "str"
        )

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        header_parameters["Content-Type"] = "application/json; charset=utf-8"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        body_content = self._serialize.body(exchange_request, "TokenExchangeRequest")

        # Construct and send request
        request = self._client.post(
            url, query_parameters, header_parameters, body_content
        )
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 400, 404]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("TokenResponse", response)
        if response.status_code == 400:
            deserialized = self._deserialize("ErrorResponse", response)
        if response.status_code == 404:
            deserialized = self._deserialize("TokenResponse", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    exchange_async.metadata = {"url": "/api/usertoken/exchange"}
