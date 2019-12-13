import aiounittest

from botframework.connector.auth import AuthenticationConstants, MicrosoftAppCredentials


class TestMicrosoftAppCredentials(aiounittest.AsyncTestCase):
    async def test_app_credentials(self):
        default_scope_case_1 = MicrosoftAppCredentials("some_app", "some_password")
        assert (
            AuthenticationConstants.TO_BOT_FROM_CHANNEL_TOKEN_ISSUER
            == default_scope_case_1.oauth_scope
        )

        # Use with default scope
        default_scope_case_2 = MicrosoftAppCredentials(
            "some_app", "some_password", "some_tenant"
        )
        assert (
            AuthenticationConstants.TO_BOT_FROM_CHANNEL_TOKEN_ISSUER
            == default_scope_case_2.oauth_scope
        )

        custom_scope = "some_scope"
        custom_scope_case_1 = MicrosoftAppCredentials(
            "some_app", "some_password", oauth_scope=custom_scope
        )
        assert custom_scope_case_1.oauth_scope == custom_scope

        # Use with default scope
        custom_scope_case_2 = MicrosoftAppCredentials(
            "some_app", "some_password", "some_tenant", custom_scope
        )
        assert custom_scope_case_2.oauth_scope == custom_scope
