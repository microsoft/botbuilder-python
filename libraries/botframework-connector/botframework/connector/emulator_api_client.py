import requests
from .auth import MicrosoftAppCredentials

class EmulatorApiClient:
    @staticmethod
    async def emulate_oauth_cards(credentials: MicrosoftAppCredentials, emulatorUrl: str, emulate: bool) -> bool:
        token = await credentials.get_token()
        requestUrl = emulatorUrl + ('' if emulatorUrl.endsWith('/') else '/') + f'api/usertoken/emulateOAuthCards?emulate={ str(emulate).lower() }'

        res = requests.post(requestUrl, headers = {
                'Authorization': f'Bearer { token }'
            })

        if res.status_code == 200:
            return True
        else:
            raise Exception(f'EmulateOAuthCards failed with status code: { res.status_code }')