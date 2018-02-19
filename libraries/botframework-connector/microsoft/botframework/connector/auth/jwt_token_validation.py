import asyncio
from microsoft.botbuilder.schema import activity

from .credential_provider import CredentialProvider
from .emulator_validation import EmulatorValidation
from .channel_validation import ChannelValidation
from .microsoft_app_credentials import MicrosoftAppCredentials

class JwtTokenValidation:
    
    @staticmethod
    async def assert_valid_activity(activity, authHeader, credentials):
        """Validates the security tokens required by the Bot Framework Protocol. Throws on any exceptions.
        activity: The incoming Activity from the Bot Framework or the Emulator
        authHeader:The Bearer token included as part of the request
        credentials: The set of valid credentials, such as the Bot Application ID
        returns Promise acception when authorized correctly, Promise rejection when not authorized.
        """
        if(not authHeader):
            # No auth header was sent. We might be on the anonymous code path.
            isAuthDisabled = await credentials.is_authentication_disabled()
            if(isAuthDisabled):
                # We are on the anonymous code path.
                return

            # No Auth Header. Auth is required. Request is not authorized.
            raise Exception('Unauthorized Access. Request is not authorized')

        usingEmulator = EmulatorValidation.is_token_from_emulator(authHeader)
        if (usingEmulator):
            await EmulatorValidation.authenticate_emulator_token(authHeader, credentials)
        else:
            await ChannelValidation.authenticate_channel_token_with_service_url(authHeader, credentials, activity.service_url)

        # On the standard Auth path, we need to trust the URL that was incoming.
        MicrosoftAppCredentials.trust_service_url(activity.service_url)