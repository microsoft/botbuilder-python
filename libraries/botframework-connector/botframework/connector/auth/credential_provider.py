class CredentialProvider:
    """CredentialProvider.
    This class allows Bots to provide their own implemention
    of what is, and what is not, a valid appId and password.
    This is useful in the case of multi-tenant bots, where the bot
    may need to call out to a service to determine if a particular
    appid/password pair is valid.
    """

    async def is_valid_appid(self, app_id: str) -> bool:
        """Validate AppId.

        This method is async to enable custom implementations
        that may need to call out to serviced to validate the appId / password pair.

        :param app_id: bot appid
        :return: true if it is a valid AppId
        """
        raise NotImplementedError

    async def get_app_password(self, app_id: str) -> str:
        """Get the app password for a given bot appId, if it is not a valid appId, return Null

        This method is async to enable custom implementations
        that may need to call out to serviced to validate the appId / password pair.

        :param app_id: bot appid
        :return: password or null for invalid appid
        """
        raise NotImplementedError

    async def is_authentication_disabled(self) -> bool:
        """Checks if bot authentication is disabled.

        Return true if bot authentication is disabled.
        This method is async to enable custom implementations
        that may need to call out to serviced to validate the appId / password pair.

        :return: true if bot authentication is disabled.
        """
        raise NotImplementedError

class SimpleCredentialProvider(CredentialProvider):
    def __init__(self, app_id: str, password: str):
        self.app_id = app_id
        self.password = password

    async def is_valid_appid(self, app_id: str) -> bool:
        return self.app_id == app_id

    async def get_app_password(self, app_id: str) -> str:
        return self.password if self.app_id == app_id else None

    async def is_authentication_disabled(self) -> bool:
        return not self.app_id
