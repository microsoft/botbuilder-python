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

    def __init__(self, *, resource_urls=None, **kwargs) -> None:
        super(AadResourceUrls, self).__init__(**kwargs)
        self.resource_urls = resource_urls


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

    def __init__(
        self, *, code: str = None, message: str = None, inner_http_error=None, **kwargs
    ) -> None:
        super(Error, self).__init__(**kwargs)
        self.code = code
        self.message = message
        self.inner_http_error = inner_http_error


class ErrorResponse(Model):
    """ErrorResponse.

    :param error:
    :type error: ~botframework.tokenapi.models.Error
    """

    _attribute_map = {"error": {"key": "error", "type": "Error"}}

    def __init__(self, *, error=None, **kwargs) -> None:
        super(ErrorResponse, self).__init__(**kwargs)
        self.error = error


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

    def __init__(self, *, status_code: int = None, body=None, **kwargs) -> None:
        super(InnerHttpError, self).__init__(**kwargs)
        self.status_code = status_code
        self.body = body


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

    def __init__(
        self, *, sign_in_link: str = None, token_exchange_resource=None, **kwargs
    ) -> None:
        super(SignInUrlResponse, self).__init__(**kwargs)
        self.sign_in_link = sign_in_link
        self.token_exchange_resource = token_exchange_resource


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

    def __init__(self, *, uri: str = None, token: str = None, **kwargs) -> None:
        super(TokenExchangeRequest, self).__init__(**kwargs)
        self.uri = uri
        self.token = token


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

    def __init__(
        self, *, id: str = None, uri: str = None, provider_id: str = None, **kwargs
    ) -> None:
        super(TokenExchangeResource, self).__init__(**kwargs)
        self.id = id
        self.uri = uri
        self.provider_id = provider_id


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

    def __init__(
        self,
        *,
        channel_id: str = None,
        connection_name: str = None,
        token: str = None,
        expiration: str = None,
        **kwargs
    ) -> None:
        super(TokenResponse, self).__init__(**kwargs)
        self.channel_id = channel_id
        self.connection_name = connection_name
        self.token = token
        self.expiration = expiration


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

    def __init__(
        self,
        *,
        channel_id: str = None,
        connection_name: str = None,
        has_token: bool = None,
        service_provider_display_name: str = None,
        **kwargs
    ) -> None:
        super(TokenStatus, self).__init__(**kwargs)
        self.channel_id = channel_id
        self.connection_name = connection_name
        self.has_token = has_token
        self.service_provider_display_name = service_provider_display_name
