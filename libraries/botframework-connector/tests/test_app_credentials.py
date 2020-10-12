# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
import requests
from botframework.connector.auth import AppCredentials, AuthenticationConstants


class AppCredentialsTests(aiounittest.AsyncTestCase):
    @staticmethod
    def test_constructor():
        should_default_to_channel_scope = AppCredentials()
        assert (
            AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
            == should_default_to_channel_scope.oauth_scope
        )

        should_default_to_custom_scope = AppCredentials(oauth_scope="customScope")
        assert "customScope" == should_default_to_custom_scope.oauth_scope

    @staticmethod
    def test_should_not_send_token_for_anonymous():
        # AppID is None
        app_creds_none = AppCredentials(app_id=None)
        assert app_creds_none._should_authorize(requests.Session()) is False

        # AppID is anonymous skill
        app_creds_anon = AppCredentials(
            app_id=AuthenticationConstants.ANONYMOUS_SKILL_APP_ID
        )
        assert app_creds_anon._should_authorize(requests.Session()) is False
