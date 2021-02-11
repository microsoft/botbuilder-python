# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class InvokeResponse:
    """
    Tuple class containing an HTTP Status Code and a JSON serializable
    object. The HTTP Status code is, in the invoke activity scenario, what will
    be set in the resulting POST. The Body of the resulting POST will be
    JSON serialized content.

    The body content is defined by the producer.  The caller must know what
    the content is and deserialize as needed.
    """

    def __init__(self, status: int = None, body: object = None):
        """
        Gets or sets the HTTP status and/or body code for the response
        :param status: The HTTP status code.
        :param body: The JSON serializable body content for the response.  This object
        must be serializable by the core Python json routines.  The caller is responsible
        for serializing more complex/nested objects into native classes (lists and
        dictionaries of strings are acceptable).
        """
        self.status = status
        self.body = body

    def is_successful_status_code(self) -> bool:
        """
        Gets a value indicating whether the invoke response was successful.
        :return: A value that indicates if the HTTP response was successful. true if status is in
        the Successful range (200-299); otherwise false.
        """
        return 200 <= self.status <= 299
