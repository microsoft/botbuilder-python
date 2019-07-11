# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import requests
from .auth import MicrosoftAppCredentials


class EmulatorApiClient:
    @staticmethod
    async def emulate_oauth_cards(
        credentials: MicrosoftAppCredentials, emulator_url: str, emulate: bool
    ) -> bool:
        token = await credentials.get_token()
        request_url = (
            emulator_url
            + ("" if emulator_url[-1] == "/" else "/")
            + f"api/usertoken/emulateOAuthCards?emulate={ str(emulate).lower() }"
        )

        res = requests.post(request_url, headers={"Authorization": f"Bearer { token }"})

        if res.status_code == 200:
            return True
        else:
            raise Exception(
                f"EmulateOAuthCards failed with status code: { res.status_code }"
            )
