# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import uuid
from typing import Dict, List, Union
from unittest.mock import Mock

import pytest

from botbuilder.schema import Activity
from botframework.connector.auth import (
    AuthenticationConfiguration,
    AuthenticationConstants,
    JwtTokenValidation,
    SimpleCredentialProvider,
    EmulatorValidation,
    EnterpriseChannelValidation,
    ChannelValidation,
    ClaimsIdentity,
    MicrosoftAppCredentials,
    GovernmentConstants,
    GovernmentChannelValidation,
    SimpleChannelProvider,
    ChannelProvider,
)


async def jwt_token_validation_validate_auth_header_with_channel_service_succeeds(
    app_id: str,
    pwd: str,
    channel_service_or_provider: Union[str, ChannelProvider],
    header: str = None,
):
    if header is None:
        header = f"Bearer {MicrosoftAppCredentials(app_id, pwd).get_access_token()}"

    credentials = SimpleCredentialProvider(app_id, pwd)
    result = await JwtTokenValidation.validate_auth_header(
        header,
        credentials,
        channel_service_or_provider,
        "",
        "https://webchat.botframework.com/",
    )

    assert result.is_authenticated


# TODO: Consider changing to unittest to use ddt for Credentials tests
class TestAuth:
    EmulatorValidation.TO_BOT_FROM_EMULATOR_TOKEN_VALIDATION_PARAMETERS.ignore_expiration = (
        True
    )
    ChannelValidation.TO_BOT_FROM_CHANNEL_TOKEN_VALIDATION_PARAMETERS.ignore_expiration = (
        True
    )

    @pytest.mark.asyncio
    async def test_claims_validation(self):
        claims: List[Dict] = []
        default_auth_config = AuthenticationConfiguration()

        # No validator should pass.
        await JwtTokenValidation.validate_claims(default_auth_config, claims)

        # ClaimsValidator configured but no exception should pass.
        mock_validator = Mock()
        auth_with_validator = AuthenticationConfiguration(
            claims_validator=mock_validator
        )

        # Configure IClaimsValidator to fail
        mock_validator.side_effect = PermissionError("Invalid claims.")
        with pytest.raises(PermissionError) as excinfo:
            await JwtTokenValidation.validate_claims(auth_with_validator, claims)

        assert "Invalid claims." in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_connector_auth_header_correct_app_id_and_service_url_should_validate(
        self,
    ):
        header = (
            "Bearer "
            + MicrosoftAppCredentials(
                "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
            ).get_access_token()
        )
        credentials = SimpleCredentialProvider(
            "2cd87869-38a0-4182-9251-d056e8f0ac24", ""
        )
        result = await JwtTokenValidation.validate_auth_header(
            header, credentials, "", "https://webchat.botframework.com/"
        )

        result_with_provider = await JwtTokenValidation.validate_auth_header(
            header,
            credentials,
            SimpleChannelProvider(),
            "https://webchat.botframework.com/",
        )

        assert result
        assert result_with_provider

    @pytest.mark.asyncio
    async def test_connector_auth_header_with_different_bot_app_id_should_not_validate(
        self,
    ):
        header = (
            "Bearer "
            + MicrosoftAppCredentials(
                "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
            ).get_access_token()
        )
        credentials = SimpleCredentialProvider(
            "00000000-0000-0000-0000-000000000000", ""
        )
        with pytest.raises(Exception) as excinfo:
            await JwtTokenValidation.validate_auth_header(
                header, credentials, "", "https://webchat.botframework.com/"
            )
        assert "Unauthorized" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo2:
            await JwtTokenValidation.validate_auth_header(
                header,
                credentials,
                SimpleChannelProvider(),
                "https://webchat.botframework.com/",
            )
        assert "Unauthorized" in str(excinfo2.value)

    @pytest.mark.asyncio
    async def test_connector_auth_header_and_no_credential_should_not_validate(self):
        header = (
            "Bearer "
            + MicrosoftAppCredentials(
                "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
            ).get_access_token()
        )
        credentials = SimpleCredentialProvider("", "")
        with pytest.raises(Exception) as excinfo:
            await JwtTokenValidation.validate_auth_header(
                header, credentials, "", "https://webchat.botframework.com/"
            )
        assert "Unauthorized" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo2:
            await JwtTokenValidation.validate_auth_header(
                header,
                credentials,
                SimpleChannelProvider(),
                "https://webchat.botframework.com/",
            )
        assert "Unauthorized" in str(excinfo2.value)

    @pytest.mark.asyncio
    async def test_empty_header_and_no_credential_should_throw(self):
        header = ""
        credentials = SimpleCredentialProvider("", "")
        with pytest.raises(Exception) as excinfo:
            await JwtTokenValidation.validate_auth_header(header, credentials, "", None)
        assert "auth_header" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo2:
            await JwtTokenValidation.validate_auth_header(
                header, credentials, SimpleChannelProvider(), None
            )
        assert "auth_header" in str(excinfo2.value)

    @pytest.mark.asyncio
    async def test_emulator_msa_header_correct_app_id_and_service_url_should_validate(
        self,
    ):
        header = (
            "Bearer "
            + MicrosoftAppCredentials(
                "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
            ).get_access_token()
        )
        credentials = SimpleCredentialProvider(
            "2cd87869-38a0-4182-9251-d056e8f0ac24", ""
        )
        result = await JwtTokenValidation.validate_auth_header(
            header, credentials, "", "https://webchat.botframework.com/"
        )

        result_with_provider = await JwtTokenValidation.validate_auth_header(
            header,
            credentials,
            SimpleChannelProvider(),
            "https://webchat.botframework.com/",
        )

        assert result
        assert result_with_provider

    @pytest.mark.asyncio
    async def test_emulator_msa_header_and_no_credential_should_not_validate(self):
        # pylint: disable=protected-access
        header = (
            "Bearer "
            + MicrosoftAppCredentials(
                "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
            ).get_access_token()
        )
        credentials = SimpleCredentialProvider(
            "00000000-0000-0000-0000-000000000000", ""
        )
        with pytest.raises(Exception) as excinfo:
            await JwtTokenValidation.validate_auth_header(header, credentials, "", None)
        assert "Unauthorized" in str(excinfo._excinfo)

        with pytest.raises(Exception) as excinfo2:
            await JwtTokenValidation.validate_auth_header(
                header, credentials, SimpleChannelProvider(), None
            )
        assert "Unauthorized" in str(excinfo2._excinfo)

    # Tests with a valid Token and service url; and ensures that Service url is added to Trusted service url list.
    @pytest.mark.asyncio
    async def test_channel_msa_header_valid_service_url_should_be_trusted(self):
        activity = Activity(
            service_url="https://smba.trafficmanager.net/amer-client-ss.msg/"
        )
        header = (
            "Bearer "
            + MicrosoftAppCredentials(
                "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
            ).get_access_token()
        )
        credentials = SimpleCredentialProvider(
            "2cd87869-38a0-4182-9251-d056e8f0ac24", ""
        )

        await JwtTokenValidation.authenticate_request(activity, header, credentials)

        assert MicrosoftAppCredentials.is_trusted_service(
            "https://smba.trafficmanager.net/amer-client-ss.msg/"
        )

    @pytest.mark.asyncio
    # Tests with a valid Token and invalid service url and ensures that Service url is NOT added to
    # Trusted service url list.
    async def test_channel_msa_header_invalid_service_url_should_not_be_trusted(self):
        activity = Activity(service_url="https://webchat.botframework.com/")
        header = (
            "Bearer "
            + MicrosoftAppCredentials(
                "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
            ).get_access_token()
        )
        credentials = SimpleCredentialProvider(
            "7f74513e-6f96-4dbc-be9d-9a81fea22b88", ""
        )

        with pytest.raises(Exception) as excinfo:
            await JwtTokenValidation.authenticate_request(activity, header, credentials)
        assert "Unauthorized" in str(excinfo.value)

        assert not MicrosoftAppCredentials.is_trusted_service(
            "https://webchat.botframework.com/"
        )

    @pytest.mark.asyncio
    async def test_channel_msa_header_from_user_specified_tenant(self):
        activity = Activity(
            service_url="https://smba.trafficmanager.net/amer-client-ss.msg/"
        )
        header = "Bearer " + MicrosoftAppCredentials(
            "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F", "microsoft.com"
        ).get_access_token(True)
        credentials = SimpleCredentialProvider(
            "2cd87869-38a0-4182-9251-d056e8f0ac24", ""
        )

        claims = await JwtTokenValidation.authenticate_request(
            activity, header, credentials
        )

        assert claims.get_claim_value("tid") == "72f988bf-86f1-41af-91ab-2d7cd011db47"

    @pytest.mark.asyncio
    # Tests with no authentication header and makes sure the service URL is not added to the trusted list.
    async def test_channel_authentication_disabled_should_be_anonymous(self):
        activity = Activity(service_url="https://webchat.botframework.com/")
        header = ""
        credentials = SimpleCredentialProvider("", "")

        claims_principal = await JwtTokenValidation.authenticate_request(
            activity, header, credentials
        )

        assert claims_principal.is_authenticated
        assert not claims_principal.claims

    @pytest.mark.asyncio
    # Tests with no authentication header and makes sure the service URL is not added to the trusted list.
    async def test_channel_authentication_disabled_service_url_should_not_be_trusted(
        self,
    ):
        activity = Activity(service_url="https://webchat.botframework.com/")
        header = ""
        credentials = SimpleCredentialProvider("", "")

        await JwtTokenValidation.authenticate_request(activity, header, credentials)

        assert not MicrosoftAppCredentials.is_trusted_service(
            "https://webchat.botframework.com/"
        )

    @pytest.mark.asyncio
    async def test_emulator_auth_header_correct_app_id_and_service_url_with_gov_channel_service_should_validate(
        self,
    ):
        await jwt_token_validation_validate_auth_header_with_channel_service_succeeds(
            "2cd87869-38a0-4182-9251-d056e8f0ac24",  # emulator creds
            "2.30Vs3VQLKt974F",
            GovernmentConstants.CHANNEL_SERVICE,
        )

        await jwt_token_validation_validate_auth_header_with_channel_service_succeeds(
            "2cd87869-38a0-4182-9251-d056e8f0ac24",  # emulator creds
            "2.30Vs3VQLKt974F",
            SimpleChannelProvider(GovernmentConstants.CHANNEL_SERVICE),
        )

    @pytest.mark.asyncio
    async def test_emulator_auth_header_correct_app_id_and_service_url_with_private_channel_service_should_validate(
        self,
    ):
        await jwt_token_validation_validate_auth_header_with_channel_service_succeeds(
            "2cd87869-38a0-4182-9251-d056e8f0ac24",  # emulator creds
            "2.30Vs3VQLKt974F",
            "TheChannel",
        )

        await jwt_token_validation_validate_auth_header_with_channel_service_succeeds(
            "2cd87869-38a0-4182-9251-d056e8f0ac24",  # emulator creds
            "2.30Vs3VQLKt974F",
            SimpleChannelProvider("TheChannel"),
        )

    @pytest.mark.asyncio
    async def test_government_channel_validation_succeeds(self):
        credentials = SimpleCredentialProvider(
            "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
        )

        await GovernmentChannelValidation.validate_identity(
            ClaimsIdentity(
                {"iss": "https://api.botframework.us", "aud": credentials.app_id}, True
            ),
            credentials,
        )

    @pytest.mark.asyncio
    async def test_government_channel_validation_no_authentication_fails(self):
        with pytest.raises(Exception) as excinfo:
            await GovernmentChannelValidation.validate_identity(
                ClaimsIdentity({}, False), None
            )
        assert "Unauthorized" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_government_channel_validation_no_issuer_fails(self):
        credentials = SimpleCredentialProvider(
            "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
        )
        with pytest.raises(Exception) as excinfo:
            await GovernmentChannelValidation.validate_identity(
                ClaimsIdentity({"peanut": "peanut"}, True), credentials
            )
        assert "Unauthorized" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_government_channel_validation_wrong_issuer_fails(self):
        credentials = SimpleCredentialProvider(
            "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
        )
        with pytest.raises(Exception) as excinfo:
            await GovernmentChannelValidation.validate_identity(
                ClaimsIdentity({"iss": "peanut"}, True), credentials
            )
        assert "Unauthorized" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_government_channel_validation_no_audience_fails(self):
        credentials = SimpleCredentialProvider(
            "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
        )
        with pytest.raises(Exception) as excinfo:
            await GovernmentChannelValidation.validate_identity(
                ClaimsIdentity({"iss": "https://api.botframework.us"}, True),
                credentials,
            )
        assert "Unauthorized" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_government_channel_validation_wrong_audience_fails(self):
        credentials = SimpleCredentialProvider(
            "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
        )
        with pytest.raises(Exception) as excinfo:
            await GovernmentChannelValidation.validate_identity(
                ClaimsIdentity(
                    {"iss": "https://api.botframework.us", "aud": "peanut"}, True
                ),
                credentials,
            )
        assert "Unauthorized" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_enterprise_channel_validation_succeeds(self):
        credentials = SimpleCredentialProvider(
            "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
        )

        await EnterpriseChannelValidation.validate_identity(
            ClaimsIdentity(
                {"iss": "https://api.botframework.com", "aud": credentials.app_id}, True
            ),
            credentials,
        )

    @pytest.mark.asyncio
    async def test_enterprise_channel_validation_no_authentication_fails(self):
        with pytest.raises(Exception) as excinfo:
            await EnterpriseChannelValidation.validate_identity(
                ClaimsIdentity({}, False), None
            )
        assert "Unauthorized" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_enterprise_channel_validation_no_issuer_fails(self):
        credentials = SimpleCredentialProvider(
            "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
        )
        with pytest.raises(Exception) as excinfo:
            await EnterpriseChannelValidation.validate_identity(
                ClaimsIdentity({"peanut": "peanut"}, True), credentials
            )
        assert "Unauthorized" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_enterprise_channel_validation_wrong_issuer_fails(self):
        credentials = SimpleCredentialProvider(
            "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
        )
        with pytest.raises(Exception) as excinfo:
            await EnterpriseChannelValidation.validate_identity(
                ClaimsIdentity({"iss": "peanut"}, True), credentials
            )
        assert "Unauthorized" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_enterprise_channel_validation_no_audience_fails(self):
        credentials = SimpleCredentialProvider(
            "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
        )
        with pytest.raises(Exception) as excinfo:
            await GovernmentChannelValidation.validate_identity(
                ClaimsIdentity({"iss": "https://api.botframework.com"}, True),
                credentials,
            )
        assert "Unauthorized" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_enterprise_channel_validation_wrong_audience_fails(self):
        credentials = SimpleCredentialProvider(
            "2cd87869-38a0-4182-9251-d056e8f0ac24", "2.30Vs3VQLKt974F"
        )
        with pytest.raises(Exception) as excinfo:
            await GovernmentChannelValidation.validate_identity(
                ClaimsIdentity(
                    {"iss": "https://api.botframework.com", "aud": "peanut"}, True
                ),
                credentials,
            )
        assert "Unauthorized" in str(excinfo.value)

    def test_get_app_id_from_claims(self):
        v1_claims = {}
        v2_claims = {}

        app_id = str(uuid.uuid4())

        # Empty list
        assert not JwtTokenValidation.get_app_id_from_claims(v1_claims)

        # AppId there but no version (assumes v1)
        v1_claims[AuthenticationConstants.APP_ID_CLAIM] = app_id
        assert JwtTokenValidation.get_app_id_from_claims(v1_claims) == app_id

        # AppId there with v1 version
        v1_claims[AuthenticationConstants.VERSION_CLAIM] = "1.0"
        assert JwtTokenValidation.get_app_id_from_claims(v1_claims) == app_id

        # v2 version but no azp
        v2_claims[AuthenticationConstants.VERSION_CLAIM] = "2.0"
        assert not JwtTokenValidation.get_app_id_from_claims(v2_claims)

        # v2 version but no azp
        v2_claims[AuthenticationConstants.AUTHORIZED_PARTY] = app_id
        assert JwtTokenValidation.get_app_id_from_claims(v2_claims) == app_id
