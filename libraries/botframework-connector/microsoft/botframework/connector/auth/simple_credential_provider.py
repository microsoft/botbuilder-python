from .credential_provider import CredentialProvider

class SimpleCredentialProvider(CredentialProvider):

    def __init__(self, app_id, password):
        self.app_id = app_id
        self.password = password
