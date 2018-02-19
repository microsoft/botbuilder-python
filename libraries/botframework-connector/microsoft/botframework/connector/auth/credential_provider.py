class CredentialProvider:
    async def is_valid_appid(self, appId):
        raise NotImplementedError

    async def get_app_password(self, appId):
        raise NotImplementedError
    
    async def is_authentication_disabled(self):
        raise NotImplementedError

class SimpleCredentialProvider(CredentialProvider):
    def __init__(self, app_id, password):
        self.app_id = app_id
        self.password = password

    async def is_valid_appid(self, appId):
        return self.app_id == appId

    async def get_app_password(self, appId):
        return self.password if self.app_id == appId else None
    
    async def is_authentication_disabled(self):
        return not self.app_id