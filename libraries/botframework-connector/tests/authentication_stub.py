from msrest.authentication import (
    BasicTokenAuthentication,
    Authentication)

class MicrosoftTokenAuthenticationStub(Authentication):
    def __init__(self, access_token):
        self.access_token = access_token

    def signed_session(self):
        basicAuthentication = BasicTokenAuthentication({ "access_token": self.access_token })
        return basicAuthentication.signed_session()