# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from msrest.pipeline import ClientRawResponse
from msrest.exceptions import HttpOperationError

from .. import models


class BotSignInOperations:
    """BotSignInOperations operations.

    You should not instantiate directly this class, but create a Client instance that will create it for you and
    attach it as attribute.

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

    def get_sign_in_url(
        self,
        state,
        code_challenge=None,
        emulator_url=None,
        final_redirect=None,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """

        :param state:
        :type state: str
        :param code_challenge:
        :type code_challenge: str
        :param emulator_url:
        :type emulator_url: str
        :param final_redirect:
        :type final_redirect: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: str or ClientRawResponse if raw=true
        :rtype: str or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.get_sign_in_url.metadata["url"]

        # Construct parameters
        query_parameters = {}
        query_parameters["state"] = self._serialize.query("state", state, "str")
        if code_challenge is not None:
            query_parameters["code_challenge"] = self._serialize.query(
                "code_challenge", code_challenge, "str"
            )
        if emulator_url is not None:
            query_parameters["emulatorUrl"] = self._serialize.query(
                "emulator_url", emulator_url, "str"
            )
        if final_redirect is not None:
            query_parameters["finalRedirect"] = self._serialize.query(
                "final_redirect", final_redirect, "str"
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
            raise HttpOperationError(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = response.content.decode("utf-8")

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    get_sign_in_url.metadata = {"url": "/api/botsignin/GetSignInUrl"}

    def get_sign_in_resource(
        self,
        state,
        code_challenge=None,
        emulator_url=None,
        final_redirect=None,
        custom_headers=None,
        raw=False,
        **operation_config
    ):
        """

        :param state:
        :type state: str
        :param code_challenge:
        :type code_challenge: str
        :param emulator_url:
        :type emulator_url: str
        :param final_redirect:
        :type final_redirect: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: SignInUrlResponse or ClientRawResponse if raw=true
        :rtype: ~botframework.tokenapi.models.SignInUrlResponse or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        # Construct URL
        url = self.get_sign_in_resource.metadata["url"]

        # Construct parameters
        query_parameters = {}
        query_parameters["state"] = self._serialize.query("state", state, "str")
        if code_challenge is not None:
            query_parameters["code_challenge"] = self._serialize.query(
                "code_challenge", code_challenge, "str"
            )
        if emulator_url is not None:
            query_parameters["emulatorUrl"] = self._serialize.query(
                "emulator_url", emulator_url, "str"
            )
        if final_redirect is not None:
            query_parameters["finalRedirect"] = self._serialize.query(
                "final_redirect", final_redirect, "str"
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
            raise HttpOperationError(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("SignInUrlResponse", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    get_sign_in_resource.metadata = {"url": "/api/botsignin/GetSignInResource"}
