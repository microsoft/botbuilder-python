# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.core import ChannelServiceHandler
from botframework.connector.auth import (
    AuthenticationConfiguration,
    ClaimsIdentity,
    SimpleCredentialProvider,
    JwtTokenValidation,
    AuthenticationConstants,
)
import botbuilder.schema


class TestChannelServiceHandler(ChannelServiceHandler):
    def __init__(self):
        self.claims_identity = None
        ChannelServiceHandler.__init__(
            self, SimpleCredentialProvider("", ""), AuthenticationConfiguration()
        )

    async def on_reply_to_activity(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity_id: str,
        activity: botbuilder.schema.Activity,
    ) -> botbuilder.schema.ResourceResponse:
        self.claims_identity = claims_identity
        return botbuilder.schema.ResourceResponse()


class ChannelServiceHandlerTests(aiounittest.AsyncTestCase):
    async def test_should_authenticate_anonymous_skill_claim(self):
        sut = TestChannelServiceHandler()
        await sut.handle_reply_to_activity(None, "123", "456", {})

        assert (
            sut.claims_identity.authentication_type
            == AuthenticationConstants.ANONYMOUS_AUTH_TYPE
        )
        assert (
            JwtTokenValidation.get_app_id_from_claims(sut.claims_identity.claims)
            == AuthenticationConstants.ANONYMOUS_SKILL_APP_ID
        )
