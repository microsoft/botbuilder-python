from .credential_provider import CredentialProvider

class SimpleCredentialProvider(CredentialProvider):

    def __init__(self, app_id, password):
        self.app_id = app_id
        self.password = password

    async def is_valid_appid(self, appId):
        return self.app_id == appId