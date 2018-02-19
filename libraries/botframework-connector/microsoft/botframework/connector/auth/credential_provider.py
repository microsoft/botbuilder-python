class CredentialProvider:
    async def is_valid_appid(self, app_id):
        raise NotImplementedError

    async def get_app_password(self, app_id):
        raise NotImplementedError

    async def is_authentication_disabled(self):
        raise NotImplementedError

class SimpleCredentialProvider(CredentialProvider):
    def __init__(self, app_id, password):
        self.app_id = app_id
        self.password = password

    async def is_valid_appid(self, app_id):
        return self.app_id == app_id

    async def get_app_password(self, app_id):
        return self.password if self.app_id == app_id else None

    async def is_authentication_disabled(self):
        return not self.app_id
