# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botframework.connector.auth import AppCredentials, AuthenticationConstants


class AppCredentialsTests(aiounittest.AsyncTestCase):
    @staticmethod
    def test_should_not_send_token_for_anonymous():
        # AppID is None
        app_creds_none = AppCredentials(app_id=None)
        assert app_creds_none.signed_session().headers.get("Authorization") is None

        # AppID is anonymous skill
        app_creds_anon = AppCredentials(
            app_id=AuthenticationConstants.ANONYMOUS_SKILL_APP_ID
        )
        assert app_creds_anon.signed_session().headers.get("Authorization") is None


def test_constructor():
    should_default_to_channel_scope = AppCredentials()
    assert (
        should_default_to_channel_scope.oauth_scope
        == AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
    )

    should_default_to_custom_scope = AppCredentials(oauth_scope="customScope")
    assert should_default_to_custom_scope.oauth_scope == "customScope"
