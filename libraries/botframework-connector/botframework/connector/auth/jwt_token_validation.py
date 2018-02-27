from botbuilder.schema import Activity

from .emulator_validation import EmulatorValidation
from .channel_validation import ChannelValidation
from .microsoft_app_credentials import MicrosoftAppCredentials
from .credential_provider import CredentialProvider

class JwtTokenValidation:

    @staticmethod
    async def assert_valid_activity(activity: Activity, auth_header: str, credentials: CredentialProvider):
        """Validates the security tokens required by the Bot Framework Protocol. Throws on any exceptions.
        
        :param activity: The incoming Activity from the Bot Framework or the Emulator
        :type activity: ~botframework.connector.models.Activity
        :param auth_header: The Bearer token included as part of the request
        :type auth_header: str
        :param credentials: The set of valid credentials, such as the Bot Application ID
        :type credentials: CredentialProvider

        :raises Exception:
        """
        if not auth_header:
            # No auth header was sent. We might be on the anonymous code path.
            is_auth_disabled = await credentials.is_authentication_disabled()
            if is_auth_disabled:
                # We are on the anonymous code path.
                return

            # No Auth Header. Auth is required. Request is not authorized.
            raise Exception('Unauthorized Access. Request is not authorized')

        using_emulator = EmulatorValidation.is_token_from_emulator(auth_header)
        if using_emulator:
            await EmulatorValidation.authenticate_emulator_token(auth_header, credentials)
        else:
            await ChannelValidation.authenticate_token_service_url(
                auth_header, credentials, activity.service_url)

        # On the standard Auth path, we need to trust the URL that was incoming.
        MicrosoftAppCredentials.trust_service_url(activity.service_url)
