# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from msrest.serialization import Model
from msrest.exceptions import HttpOperationError

# pylint: disable=invalid-name


class AadResourceUrls(Model):
    """AadResourceUrls.

    :param resource_urls:
    :type resource_urls: list[str]
    """

    _attribute_map = {"resource_urls": {"key": "resourceUrls", "type": "[str]"}}

    def __init__(self, **kwargs):
        super(AadResourceUrls, self).__init__(**kwargs)
        self.resource_urls = kwargs.get("resource_urls", None)


class Error(Model):
    """Error.

    :param code:
    :type code: str
    :param message:
    :type message: str
    :param inner_http_error:
    :type inner_http_error: ~botframework.tokenapi.models.InnerHttpError
    """

    _attribute_map = {
        "code": {"key": "code", "type": "str"},
        "message": {"key": "message", "type": "str"},
        "inner_http_error": {"key": "innerHttpError", "type": "InnerHttpError"},
    }

    def __init__(self, **kwargs):
        super(Error, self).__init__(**kwargs)
        self.code = kwargs.get("code", None)
        self.message = kwargs.get("message", None)
        self.inner_http_error = kwargs.get("inner_http_error", None)


class ErrorResponse(Model):
    """ErrorResponse.

    :param error:
    :type error: ~botframework.tokenapi.models.Error
    """

    _attribute_map = {"error": {"key": "error", "type": "Error"}}

    def __init__(self, **kwargs):
        super(ErrorResponse, self).__init__(**kwargs)
        self.error = kwargs.get("error", None)


class ErrorResponseException(HttpOperationError):
    """Server responsed with exception of type: 'ErrorResponse'.

    :param deserialize: A deserializer
    :param response: Server response to be deserialized.
    """

    def __init__(self, deserialize, response, *args):
        super(ErrorResponseException, self).__init__(
            deserialize, response, "ErrorResponse", *args
        )


class InnerHttpError(Model):
    """InnerHttpError.

    :param status_code:
    :type status_code: int
    :param body:
    :type body: object
    """

    _attribute_map = {
        "status_code": {"key": "statusCode", "type": "int"},
        "body": {"key": "body", "type": "object"},
    }

    def __init__(self, **kwargs):
        super(InnerHttpError, self).__init__(**kwargs)
        self.status_code = kwargs.get("status_code", None)
        self.body = kwargs.get("body", None)


class SignInUrlResponse(Model):
    """SignInUrlResponse.

    :param sign_in_link:
    :type sign_in_link: str
    :param token_exchange_resource:
    :type token_exchange_resource:
     ~botframework.tokenapi.models.TokenExchangeResource
    """

    _attribute_map = {
        "sign_in_link": {"key": "signInLink", "type": "str"},
        "token_exchange_resource": {
            "key": "tokenExchangeResource",
            "type": "TokenExchangeResource",
        },
    }

    def __init__(self, **kwargs):
        super(SignInUrlResponse, self).__init__(**kwargs)
        self.sign_in_link = kwargs.get("sign_in_link", None)
        self.token_exchange_resource = kwargs.get("token_exchange_resource", None)


class TokenExchangeRequest(Model):
    """TokenExchangeRequest.

    :param uri:
    :type uri: str
    :param token:
    :type token: str
    """

    _attribute_map = {
        "uri": {"key": "uri", "type": "str"},
        "token": {"key": "token", "type": "str"},
    }

    def __init__(self, **kwargs):
        super(TokenExchangeRequest, self).__init__(**kwargs)
        self.uri = kwargs.get("uri", None)
        self.token = kwargs.get("token", None)


class TokenExchangeResource(Model):
    """TokenExchangeResource.

    :param id:
    :type id: str
    :param uri:
    :type uri: str
    :param provider_id:
    :type provider_id: str
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "uri": {"key": "uri", "type": "str"},
        "provider_id": {"key": "providerId", "type": "str"},
    }

    def __init__(self, **kwargs):
        super(TokenExchangeResource, self).__init__(**kwargs)
        self.id = kwargs.get("id", None)
        self.uri = kwargs.get("uri", None)
        self.provider_id = kwargs.get("provider_id", None)


class TokenResponse(Model):
    """TokenResponse.

    :param channel_id:
    :type channel_id: str
    :param connection_name:
    :type connection_name: str
    :param token:
    :type token: str
    :param expiration:
    :type expiration: str
    """

    _attribute_map = {
        "channel_id": {"key": "channelId", "type": "str"},
        "connection_name": {"key": "connectionName", "type": "str"},
        "token": {"key": "token", "type": "str"},
        "expiration": {"key": "expiration", "type": "str"},
    }

    def __init__(self, **kwargs):
        super(TokenResponse, self).__init__(**kwargs)
        self.channel_id = kwargs.get("channel_id", None)
        self.connection_name = kwargs.get("connection_name", None)
        self.token = kwargs.get("token", None)
        self.expiration = kwargs.get("expiration", None)


class TokenStatus(Model):
    """The status of a particular token.

    :param channel_id: The channelId of the token status pertains to
    :type channel_id: str
    :param connection_name: The name of the connection the token status
     pertains to
    :type connection_name: str
    :param has_token: True if a token is stored for this ConnectionName
    :type has_token: bool
    :param service_provider_display_name: The display name of the service
     provider for which this Token belongs to
    :type service_provider_display_name: str
    """

    _attribute_map = {
        "channel_id": {"key": "channelId", "type": "str"},
        "connection_name": {"key": "connectionName", "type": "str"},
        "has_token": {"key": "hasToken", "type": "bool"},
        "service_provider_display_name": {
            "key": "serviceProviderDisplayName",
            "type": "str",
        },
    }

    def __init__(self, **kwargs):
        super(TokenStatus, self).__init__(**kwargs)
        self.channel_id = kwargs.get("channel_id", None)
        self.connection_name = kwargs.get("connection_name", None)
        self.has_token = kwargs.get("has_token", None)
        self.service_provider_display_name = kwargs.get(
            "service_provider_display_name", None
        )
