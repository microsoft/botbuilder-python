# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class Authenticator:
    """
    A provider of tokens
    """

    def acquire_token(self):
        """
        Returns a token.  The implementation is supplied by a subclass.
        :return: The string token
        """
        raise NotImplementedError()
