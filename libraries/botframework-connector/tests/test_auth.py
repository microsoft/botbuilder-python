import pytest

from botbuilder.schema import Activity
from botframework.connector.auth import JwtTokenValidation
from botframework.connector.auth import SimpleCredentialProvider
from botframework.connector.auth import EmulatorValidation
from botframework.connector.auth import ChannelValidation
from botframework.connector.auth import MicrosoftAppCredentials


class TestAuth:
    EmulatorValidation.TO_BOT_FROM_EMULATOR_TOKEN_VALIDATION_PARAMETERS.ignore_expiration = True
    ChannelValidation.TO_BOT_FROM_CHANNEL_TOKEN_VALIDATION_PARAMETERS.ignore_expiration = True
    
    @pytest.mark.asyncio
    async def test_connector_auth_header_correct_app_id_and_service_url_should_validate(self):
        header = 'Bearer ' + MicrosoftAppCredentials('2cd87869-38a0-4182-9251-d056e8f0ac24', '2.30Vs3VQLKt974F').get_access_token()
        credentials = SimpleCredentialProvider('2cd87869-38a0-4182-9251-d056e8f0ac24', '')
        result = await JwtTokenValidation.validate_auth_header(header, credentials, '', 'https://webchat.botframework.com/')

        assert result

    @pytest.mark.asyncio
    async def test_connector_auth_header_with_different_bot_app_id_should_not_validate(self):
        header = 'Bearer ' + MicrosoftAppCredentials('2cd87869-38a0-4182-9251-d056e8f0ac24', '2.30Vs3VQLKt974F').get_access_token()
        credentials = SimpleCredentialProvider('00000000-0000-0000-0000-000000000000', '')
        with pytest.raises(Exception) as excinfo:
            await JwtTokenValidation.validate_auth_header(header, credentials, '', 'https://webchat.botframework.com/')
        assert 'Unauthorized' in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_connector_auth_header_and_no_credential_should_not_validate(self):
        header = 'Bearer ' + MicrosoftAppCredentials('2cd87869-38a0-4182-9251-d056e8f0ac24', '2.30Vs3VQLKt974F').get_access_token()
        credentials = SimpleCredentialProvider('', '')
        with pytest.raises(Exception) as excinfo:
            await JwtTokenValidation.validate_auth_header(header, credentials, '', 'https://webchat.botframework.com/')
        assert 'Unauthorized' in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_empty_header_and_no_credential_should_validate(self):
        header = ''
        credentials = SimpleCredentialProvider('', '')
        with pytest.raises(Exception) as excinfo:
            await JwtTokenValidation.validate_auth_header(header, credentials, '', None)
        assert 'auth_header' in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_emulator_msa_header_correct_app_id_and_service_url_should_validate(self):
        header = 'Bearer ' + MicrosoftAppCredentials('2cd87869-38a0-4182-9251-d056e8f0ac24', '2.30Vs3VQLKt974F').get_access_token()
        credentials = SimpleCredentialProvider('2cd87869-38a0-4182-9251-d056e8f0ac24', '')
        result = await JwtTokenValidation.validate_auth_header(header, credentials, '', 'https://webchat.botframework.com/')

        assert result

    @pytest.mark.asyncio
    async def test_emulator_msa_header_and_no_credential_should_not_validate(self):
        header = 'Bearer ' + MicrosoftAppCredentials('2cd87869-38a0-4182-9251-d056e8f0ac24', '2.30Vs3VQLKt974F').get_access_token()
        credentials = SimpleCredentialProvider('00000000-0000-0000-0000-000000000000', '')
        with pytest.raises(Exception) as excinfo:
            await JwtTokenValidation.validate_auth_header(header, credentials, '', None)
            assert 'Unauthorized' in excinfo

    @pytest.mark.asyncio
    # Tests with a valid Token and service url; and ensures that Service url is added to Trusted service url list.
    async def test_channel_msa_header_Valid_service_url_should_be_trusted(self):
        activity = Activity(service_url = 'https://smba.trafficmanager.net/amer-client-ss.msg/')
        header = 'Bearer ' + MicrosoftAppCredentials('2cd87869-38a0-4182-9251-d056e8f0ac24', '2.30Vs3VQLKt974F').get_access_token()
        credentials = SimpleCredentialProvider('2cd87869-38a0-4182-9251-d056e8f0ac24', '')

        await JwtTokenValidation.authenticate_request(activity, header, credentials)

        assert MicrosoftAppCredentials.is_trusted_service('https://smba.trafficmanager.net/amer-client-ss.msg/')
    
    @pytest.mark.asyncio
    # Tests with a valid Token and invalid service url; and ensures that Service url is NOT added to Trusted service url list.
    async def test_channel_msa_header_invalid_service_url_should_not_be_trusted(self):
        activity = Activity(service_url = 'https://webchat.botframework.com/')
        header = 'Bearer ' + MicrosoftAppCredentials('2cd87869-38a0-4182-9251-d056e8f0ac24', '2.30Vs3VQLKt974F').get_access_token()
        credentials = SimpleCredentialProvider('7f74513e-6f96-4dbc-be9d-9a81fea22b88', '')

        with pytest.raises(Exception) as excinfo:
            await JwtTokenValidation.authenticate_request(activity, header, credentials)
        assert 'Unauthorized' in str(excinfo.value)
        
        assert not MicrosoftAppCredentials.is_trusted_service('https://webchat.botframework.com/')
    
    @pytest.mark.asyncio
    # Tests with no authentication header and makes sure the service URL is not added to the trusted list.
    async def test_channel_authentication_disabled_should_be_anonymous(self):
        activity = Activity(service_url = 'https://webchat.botframework.com/')
        header = ''
        credentials = SimpleCredentialProvider('', '')

        claimsPrincipal = await JwtTokenValidation.authenticate_request(activity, header, credentials)

        assert claimsPrincipal == None
    
    @pytest.mark.asyncio
    # Tests with no authentication header and makes sure the service URL is not added to the trusted list.
    async def test_channel_authentication_disabled_service_url_should_not_be_trusted(self):
        activity = Activity(service_url = 'https://webchat.botframework.com/')
        header = ''
        credentials = SimpleCredentialProvider('', '')

        await JwtTokenValidation.authenticate_request(activity, header, credentials)

        assert not MicrosoftAppCredentials.is_trusted_service('https://webchat.botframework.com/')