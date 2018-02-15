import asyncio
from microsoft.botbuilder.schema import activity

from .credentialProvider import ICredentialProvider
from .emulatorValidation import EmulatorValidation
from .channelValidation import ChannelValidation
from .microsoftAppCredentials import MicrosoftAppCredentials

class JwtTokenValidation:
    async def assertValidActivity(self, activity, authHeader, credentials):
        """Validates the security tokens required by the Bot Framework Protocol. Throws on any exceptions.
        activity: The incoming Activity from the Bot Framework or the Emulator
        authHeader:The Bearer token included as part of the request
        credentials: The set of valid credentials, such as the Bot Application ID
        returns Promise acception when authorized correctly, Promise rejection when not authorized.
        """
        if(not authHeader):
            # No auth header was sent. We might be on the anonymous code path.
            isAuthDisabled = await credentials.isAuthenticationDisabled()
            if(isAuthDisabled):
                # We are on the anonymous code path.
                return

            # No Auth Header. Auth is required. Request is not authorized.
            raise Exception('Unauthorized Access. Request is not authorized')

        usingEmulator = EmulatorValidation.isTokenFromEmulator(authHeader)
        if (usingEmulator):
            await asyncio.ensure_future(EmulatorValidation.authenticateEmulatorToken(authHeader, credentials))
        else:
            await asyncio.ensure_future(ChannelValidation.authenticateChannelTokenWithServiceUrl(authHeader, credentials, activity.serviceUrl))

        # On the standard Auth path, we need to trust the URL that was incoming.
        MicrosoftAppCredentials.trustServiceUrl(activity.serviceUrl)