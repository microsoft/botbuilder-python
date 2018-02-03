from msrest.authentication import (
    BasicTokenAuthentication,
    Authentication)

import requests
from datetime import  datetime, timedelta
import json

AuthSettings = {
    "refreshEndpoint": 'https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token',
    "refreshScope": 'https://api.botframework.com/.default',
    "botConnectorOpenIdMetadata": 'https://login.botframework.com/v1/.well-known/openidconfiguration',
    "botConnectorIssuer": 'https://api.botframework.com',
    "emulatorOpenIdMetadata": 'https://login.microsoftonline.com/botframework.com/v2.0/.well-known/openid-configuration',
    "emulatorAuthV31IssuerV1": 'https://sts.windows.net/d6d49420-f39b-4df7-a1dc-d59a935871db/',
    "emulatorAuthV31IssuerV2": 'https://login.microsoftonline.com/d6d49420-f39b-4df7-a1dc-d59a935871db/v2.0',
    "emulatorAuthV32IssuerV1": 'https://sts.windows.net/f8cdef31-a31e-4b4a-93e4-5f571e91255a/',
    "emulatorAuthV32IssuerV2": 'https://login.microsoftonline.com/f8cdef31-a31e-4b4a-93e4-5f571e91255a/v2.0'
}

class MicrosoftTokenAuthentication(Authentication):
    def __init__(self, appId, password):
        self.microsoftAppId = appId
        self.microsoftAppPassword = password
        self.scheme = 'Bearer'
        self.token = ""
        self.accessTokenExpiration = datetime.min

    def signed_session(self):
        basicAuthentication = BasicTokenAuthentication({"access_token": self.get_accessToken()})
        return  basicAuthentication.signed_session()

    def get_accessToken(self):
        if(self.microsoftAppId and self.microsoftAppPassword):
            if((not self.token) or (datetime.now() >= self.accessTokenExpiration) ):
                options = {'grant_type': 'client_credentials', \
                    'client_id': self.microsoftAppId, \
                    'client_secret': self.microsoftAppPassword, \
                   'scope': AuthSettings["refreshScope"] }
                response = requests.post(AuthSettings["refreshEndpoint"],data=options)
                response.raise_for_status()
                oauthResponse = response.json()
                self.token = oauthResponse["access_token"]
                self.accessTokenExpiration = datetime.now() + timedelta(seconds= (oauthResponse["expires_in"] - 300))
        return self.token