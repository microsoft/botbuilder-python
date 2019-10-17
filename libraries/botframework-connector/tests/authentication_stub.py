# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.authentication import BasicTokenAuthentication, Authentication


class MicrosoftTokenAuthenticationStub(Authentication):
    def __init__(self, access_token):
        self.access_token = access_token

    def signed_session(self, session=None):
        basic_authentication = BasicTokenAuthentication(
            {"access_token": self.access_token}
        )
        return session or basic_authentication.signed_session()
