# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class InvokeResponse:
    """
    Tuple class containing an HTTP Status Code and a JSON Serializable
    object. The HTTP Status code is, in the invoke activity scenario, what will
    be set in the resulting POST. The Body of the resulting POST will be
    the JSON Serialized content from the Body property.
    """

    def __init__(self, status: int = None, body: object = None):
        """
        Gets or sets the HTTP status and/or body code for the response
        :param status: The HTTP status code.
        :param body: The body content for the response.
        """
        self.status = status
        self.body = body
