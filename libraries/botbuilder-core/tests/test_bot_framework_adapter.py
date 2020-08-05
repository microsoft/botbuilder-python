# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from copy import copy, deepcopy
from unittest.mock import Mock
import unittest
import uuid
import aiounittest

from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext,
)
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ConversationAccount,
    ConversationReference,
    ConversationResourceResponse,
    ChannelAccount,
    DeliveryModes,
    ExpectedReplies,
    CallerIdConstants,
)
from botframework.connector.aio import ConnectorClient
from botframework.connector.auth import (
    ClaimsIdentity,
    AuthenticationConstants,
    AppCredentials,
    CredentialProvider,
    SimpleChannelProvider,
    GovernmentConstants,
    SimpleCredentialProvider,
)

REFERENCE = ConversationReference(
    activity_id="1234",
    channel_id="test",
    locale="en-uS",  # Intentionally oddly-cased to check that it isn't defaulted somewhere, but tests stay in English
    service_url="https://example.org/channel",
    user=ChannelAccount(id="user", name="User Name"),
    bot=ChannelAccount(id="bot", name="Bot Name"),
    conversation=ConversationAccount(id="convo1"),
)

TEST_ACTIVITY = Activity(text="test", type=ActivityTypes.message)

INCOMING_MESSAGE = TurnContext.apply_conversation_reference(
    copy(TEST_ACTIVITY), REFERENCE, True
)
OUTGOING_MESSAGE = TurnContext.apply_conversation_reference(
    copy(TEST_ACTIVITY), REFERENCE
)
INCOMING_INVOKE = TurnContext.apply_conversation_reference(
    Activity(type=ActivityTypes.invoke), REFERENCE, True
)


class AdapterUnderTest(BotFrameworkAdapter):
    def __init__(self, settings=None):
        super().__init__(settings)
        self.tester = aiounittest.AsyncTestCase()
        self.fail_auth = False
        self.fail_operation = False
        self.expect_auth_header = ""
        self.new_service_url = None
        self.connector_client_mock = None

    def aux_test_authenticate_request(self, request: Activity, auth_header: str):
        return super()._authenticate_request(request, auth_header)

    async def aux_test_create_connector_client(self, service_url: str):
        return await super().create_connector_client(service_url)

    async def _authenticate_request(
        self, request: Activity, auth_header: str
    ) -> ClaimsIdentity:
        self.tester.assertIsNotNone(
            request, "authenticate_request() not passed request."
        )
        self.tester.assertEqual(
            auth_header,
            self.expect_auth_header,
            "authenticateRequest() not passed expected authHeader.",
        )

        if self.fail_auth:
            raise PermissionError("Unauthorized Access. Request is not authorized")

        return ClaimsIdentity(
            claims={
                AuthenticationConstants.AUDIENCE_CLAIM: self.settings.app_id,
                AuthenticationConstants.APP_ID_CLAIM: self.settings.app_id,
            },
            is_authenticated=True,
        )

    async def create_connector_client(
        self,
        service_url: str,
        identity: ClaimsIdentity = None,  # pylint: disable=unused-argument
        audience: str = None,  # pylint: disable=unused-argument
    ) -> ConnectorClient:
        return self._get_or_create_connector_client(service_url, None)

    def _get_or_create_connector_client(
        self, service_url: str, credentials: AppCredentials
    ) -> ConnectorClient:
        self.tester.assertIsNotNone(
            service_url, "create_connector_client() not passed service_url."
        )

        if self.connector_client_mock:
            return self.connector_client_mock
        self.connector_client_mock = Mock()

        async def mock_reply_to_activity(conversation_id, activity_id, activity):
            nonlocal self
            self.tester.assertIsNotNone(
                conversation_id, "reply_to_activity not passed conversation_id"
            )
            self.tester.assertIsNotNone(
                activity_id, "reply_to_activity not passed activity_id"
            )
            self.tester.assertIsNotNone(
                activity, "reply_to_activity not passed activity"
            )
            return not self.fail_auth

        async def mock_send_to_conversation(conversation_id, activity):
            nonlocal self
            self.tester.assertIsNotNone(
                conversation_id, "send_to_conversation not passed conversation_id"
            )
            self.tester.assertIsNotNone(
                activity, "send_to_conversation not passed activity"
            )
            return not self.fail_auth

        async def mock_update_activity(conversation_id, activity_id, activity):
            nonlocal self
            self.tester.assertIsNotNone(
                conversation_id, "update_activity not passed conversation_id"
            )
            self.tester.assertIsNotNone(
                activity_id, "update_activity not passed activity_id"
            )
            self.tester.assertIsNotNone(activity, "update_activity not passed activity")
            return not self.fail_auth

        async def mock_delete_activity(conversation_id, activity_id):
            nonlocal self
            self.tester.assertIsNotNone(
                conversation_id, "delete_activity not passed conversation_id"
            )
            self.tester.assertIsNotNone(
                activity_id, "delete_activity not passed activity_id"
            )
            return not self.fail_auth

        async def mock_create_conversation(parameters):
            nonlocal self
            self.tester.assertIsNotNone(
                parameters, "create_conversation not passed parameters"
            )
            response = ConversationResourceResponse(
                activity_id=REFERENCE.activity_id,
                service_url=REFERENCE.service_url,
                id=uuid.uuid4(),
            )
            return response

        self.connector_client_mock.conversations.reply_to_activity.side_effect = (
            mock_reply_to_activity
        )
        self.connector_client_mock.conversations.send_to_conversation.side_effect = (
            mock_send_to_conversation
        )
        self.connector_client_mock.conversations.update_activity.side_effect = (
            mock_update_activity
        )
        self.connector_client_mock.conversations.delete_activity.side_effect = (
            mock_delete_activity
        )
        self.connector_client_mock.conversations.create_conversation.side_effect = (
            mock_create_conversation
        )

        return self.connector_client_mock


async def process_activity(
    channel_id: str, channel_data_tenant_id: str, conversation_tenant_id: str
):
    activity = None
    mock_claims = unittest.mock.create_autospec(ClaimsIdentity)
    mock_credential_provider = unittest.mock.create_autospec(
        BotFrameworkAdapterSettings
    )

    sut = BotFrameworkAdapter(mock_credential_provider)

    async def aux_func(context):
        nonlocal activity
        activity = context.Activity

    await sut.process_activity(
        Activity(
            channel_id=channel_id,
            service_url="https://smba.trafficmanager.net/amer/",
            channel_data={"tenant": {"id": channel_data_tenant_id}},
            conversation=ConversationAccount(tenant_id=conversation_tenant_id),
        ),
        mock_claims,
        aux_func,
    )
    return activity


class TestBotFrameworkAdapter(aiounittest.AsyncTestCase):
    async def test_should_create_connector_client(self):
        adapter = AdapterUnderTest()
        client = await adapter.aux_test_create_connector_client(REFERENCE.service_url)
        self.assertIsNotNone(client, "client not returned.")
        self.assertIsNotNone(client.conversations, "invalid client returned.")

    async def test_should_process_activity(self):
        called = False
        adapter = AdapterUnderTest()

        async def aux_func_assert_context(context):
            self.assertIsNotNone(context, "context not passed.")
            nonlocal called
            called = True

        await adapter.process_activity(INCOMING_MESSAGE, "", aux_func_assert_context)
        self.assertTrue(called, "bot logic not called.")

    async def test_should_fail_to_update_activity_if_service_url_missing(self):
        adapter = AdapterUnderTest()
        context = TurnContext(adapter, INCOMING_MESSAGE)
        cpy = deepcopy(INCOMING_MESSAGE)
        cpy.service_url = None
        with self.assertRaises(Exception) as _:
            await adapter.update_activity(context, cpy)

    async def test_should_fail_to_update_activity_if_conversation_missing(self):
        adapter = AdapterUnderTest()
        context = TurnContext(adapter, INCOMING_MESSAGE)
        cpy = deepcopy(INCOMING_MESSAGE)
        cpy.conversation = None
        with self.assertRaises(Exception) as _:
            await adapter.update_activity(context, cpy)

    async def test_should_fail_to_update_activity_if_activity_id_missing(self):
        adapter = AdapterUnderTest()
        context = TurnContext(adapter, INCOMING_MESSAGE)
        cpy = deepcopy(INCOMING_MESSAGE)
        cpy.id = None
        with self.assertRaises(Exception) as _:
            await adapter.update_activity(context, cpy)

    async def test_should_migrate_tenant_id_for_msteams(self):
        incoming = TurnContext.apply_conversation_reference(
            activity=Activity(
                type=ActivityTypes.message,
                text="foo",
                channel_data={"tenant": {"id": "1234"}},
            ),
            reference=REFERENCE,
            is_incoming=True,
        )

        incoming.channel_id = "msteams"
        adapter = AdapterUnderTest()

        async def aux_func_assert_tenant_id_copied(context):
            self.assertEqual(
                context.activity.conversation.tenant_id,
                "1234",
                "should have copied tenant id from "
                "channel_data to conversation address",
            )

        await adapter.process_activity(incoming, "", aux_func_assert_tenant_id_copied)

    async def test_should_create_valid_conversation_for_msteams(self):

        tenant_id = "testTenant"

        reference = deepcopy(REFERENCE)
        reference.conversation.tenant_id = tenant_id
        reference.channel_data = {"tenant": {"id": tenant_id}}
        adapter = AdapterUnderTest()

        called = False

        async def aux_func_assert_valid_conversation(context):
            self.assertIsNotNone(context, "context not passed")
            self.assertIsNotNone(context.activity, "context has no request")
            self.assertIsNotNone(
                context.activity.conversation, "request has invalid conversation"
            )
            self.assertEqual(
                context.activity.conversation.tenant_id,
                tenant_id,
                "request has invalid tenant_id on conversation",
            )
            self.assertEqual(
                context.activity.channel_data["tenant"]["tenantId"],
                tenant_id,
                "request has invalid tenant_id in channel_data",
            )
            nonlocal called
            called = True

        await adapter.create_conversation(reference, aux_func_assert_valid_conversation)
        self.assertTrue(called, "bot logic not called.")

    @staticmethod
    def get_creds_and_assert_values(
        turn_context: TurnContext,
        expected_app_id: str,
        expected_scope: str,
        creds_count: int,
    ):
        if creds_count > 0:
            # pylint: disable=protected-access
            credential_cache = turn_context.adapter._app_credential_map
            cache_key = BotFrameworkAdapter.key_for_app_credentials(
                expected_app_id, expected_scope
            )
            credentials = credential_cache.get(cache_key)
            assert credentials

            TestBotFrameworkAdapter.assert_credentials_values(
                credentials, expected_app_id, expected_scope
            )

            if creds_count:
                assert creds_count == len(credential_cache)

    @staticmethod
    def get_client_and_assert_values(
        turn_context: TurnContext,
        expected_app_id: str,
        expected_scope: str,
        expected_url: str,
        client_count: int,
    ):
        # pylint: disable=protected-access
        client_cache = turn_context.adapter._connector_client_cache
        cache_key = BotFrameworkAdapter.key_for_connector_client(
            expected_url, expected_app_id, expected_scope
        )
        client = client_cache.get(cache_key)
        assert client

        TestBotFrameworkAdapter.assert_connectorclient_vaules(
            client, expected_app_id, expected_url, expected_scope
        )

        assert client_count == len(client_cache)

    @staticmethod
    def assert_connectorclient_vaules(
        client: ConnectorClient,
        expected_app_id,
        expected_service_url: str,
        expected_scope=AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
    ):
        creds = client.config.credentials
        assert TestBotFrameworkAdapter.__str_equal(
            expected_app_id, creds.microsoft_app_id
        )
        assert TestBotFrameworkAdapter.__str_equal(expected_scope, creds.oauth_scope)
        assert TestBotFrameworkAdapter.__str_equal(
            expected_service_url, client.config.base_url
        )

    @staticmethod
    def __str_equal(str1: str, str2: str) -> bool:
        return (str1 if str1 is not None else "") == (str2 if str2 is not None else "")

    @staticmethod
    def assert_credentials_values(
        credentials: AppCredentials,
        expected_app_id: str,
        expected_scope: str = AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
    ):
        assert expected_app_id == credentials.microsoft_app_id
        assert expected_scope == credentials.oauth_scope

    async def test_process_activity_creates_correct_creds_and_client_channel_to_bot(
        self,
    ):
        await self.__process_activity_creates_correct_creds_and_client(
            None,
            None,
            None,
            AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
            0,
            1,
        )

    async def test_process_activity_creates_correct_creds_and_client_public_azure(self):
        await self.__process_activity_creates_correct_creds_and_client(
            "00000000-0000-0000-0000-000000000001",
            CallerIdConstants.public_azure_channel,
            None,
            AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
            1,
            1,
        )

    async def test_process_activity_creates_correct_creds_and_client_us_gov(self):
        await self.__process_activity_creates_correct_creds_and_client(
            "00000000-0000-0000-0000-000000000001",
            CallerIdConstants.us_gov_channel,
            GovernmentConstants.CHANNEL_SERVICE,
            GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
            1,
            1,
        )

    async def __process_activity_creates_correct_creds_and_client(
        self,
        bot_app_id: str,
        expected_caller_id: str,
        channel_service: str,
        expected_scope: str,
        expected_app_credentials_count: int,
        expected_client_credentials_count: int,
    ):
        identity = ClaimsIdentity({}, True)
        if bot_app_id:
            identity.claims = {
                AuthenticationConstants.AUDIENCE_CLAIM: bot_app_id,
                AuthenticationConstants.APP_ID_CLAIM: bot_app_id,
                AuthenticationConstants.VERSION_CLAIM: "1.0",
            }

        credential_provider = SimpleCredentialProvider(bot_app_id, None)
        service_url = "https://smba.trafficmanager.net/amer/"

        async def callback(context: TurnContext):
            TestBotFrameworkAdapter.get_creds_and_assert_values(
                context, bot_app_id, expected_scope, expected_app_credentials_count,
            )
            TestBotFrameworkAdapter.get_client_and_assert_values(
                context,
                bot_app_id,
                expected_scope,
                service_url,
                expected_client_credentials_count,
            )

            assert context.activity.caller_id == expected_caller_id

        settings = BotFrameworkAdapterSettings(
            bot_app_id,
            credential_provider=credential_provider,
            channel_provider=SimpleChannelProvider(channel_service),
        )
        sut = BotFrameworkAdapter(settings)
        await sut.process_activity_with_identity(
            Activity(channel_id="emulator", service_url=service_url, text="test",),
            identity,
            callback,
        )

    async def test_process_activity_for_forwarded_activity(self):
        bot_app_id = "00000000-0000-0000-0000-000000000001"
        skill_1_app_id = "00000000-0000-0000-0000-000000skill1"
        identity = ClaimsIdentity(
            claims={
                AuthenticationConstants.AUDIENCE_CLAIM: skill_1_app_id,
                AuthenticationConstants.APP_ID_CLAIM: bot_app_id,
                AuthenticationConstants.VERSION_CLAIM: "1.0",
            },
            is_authenticated=True,
        )

        service_url = "https://root-bot.test.azurewebsites.net/"

        async def callback(context: TurnContext):
            TestBotFrameworkAdapter.get_creds_and_assert_values(
                context, skill_1_app_id, bot_app_id, 1,
            )
            TestBotFrameworkAdapter.get_client_and_assert_values(
                context, skill_1_app_id, bot_app_id, service_url, 1,
            )

            scope = context.turn_state[BotFrameworkAdapter.BOT_OAUTH_SCOPE_KEY]
            assert bot_app_id == scope
            assert (
                context.activity.caller_id
                == f"{CallerIdConstants.bot_to_bot_prefix}{bot_app_id}"
            )

        settings = BotFrameworkAdapterSettings(bot_app_id)
        sut = BotFrameworkAdapter(settings)
        await sut.process_activity_with_identity(
            Activity(channel_id="emulator", service_url=service_url, text="test",),
            identity,
            callback,
        )

    async def test_continue_conversation_without_audience(self):
        mock_credential_provider = unittest.mock.create_autospec(CredentialProvider)

        settings = BotFrameworkAdapterSettings(
            app_id="bot_id", credential_provider=mock_credential_provider
        )
        adapter = BotFrameworkAdapter(settings)

        skill_1_app_id = "00000000-0000-0000-0000-000000skill1"
        skill_2_app_id = "00000000-0000-0000-0000-000000skill2"

        skills_identity = ClaimsIdentity(
            claims={
                AuthenticationConstants.AUDIENCE_CLAIM: skill_1_app_id,
                AuthenticationConstants.APP_ID_CLAIM: skill_2_app_id,
                AuthenticationConstants.VERSION_CLAIM: "1.0",
            },
            is_authenticated=True,
        )

        channel_service_url = "https://smba.trafficmanager.net/amer/"

        async def callback(context: TurnContext):
            TestBotFrameworkAdapter.get_creds_and_assert_values(
                context,
                skill_1_app_id,
                AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
                1,
            )
            TestBotFrameworkAdapter.get_client_and_assert_values(
                context,
                skill_1_app_id,
                AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
                channel_service_url,
                1,
            )

            # pylint: disable=protected-access
            client_cache = context.adapter._connector_client_cache
            client = client_cache.get(
                BotFrameworkAdapter.key_for_connector_client(
                    channel_service_url,
                    skill_1_app_id,
                    AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
                )
            )
            assert client

            turn_state_client = context.turn_state.get(
                BotFrameworkAdapter.BOT_CONNECTOR_CLIENT_KEY
            )
            assert turn_state_client
            client_creds = turn_state_client.config.credentials

            assert skill_1_app_id == client_creds.microsoft_app_id
            assert (
                AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
                == client_creds.oauth_scope
            )
            assert client.config.base_url == turn_state_client.config.base_url

            scope = context.turn_state[BotFrameworkAdapter.BOT_OAUTH_SCOPE_KEY]
            assert AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE == scope

            # Ensure the serviceUrl was added to the trusted hosts
            assert AppCredentials.is_trusted_service(channel_service_url)

        refs = ConversationReference(service_url=channel_service_url)

        # Ensure the serviceUrl is NOT in the trusted hosts
        assert not AppCredentials.is_trusted_service(channel_service_url)

        await adapter.continue_conversation(
            refs, callback, claims_identity=skills_identity
        )

    async def test_continue_conversation_with_audience(self):
        mock_credential_provider = unittest.mock.create_autospec(CredentialProvider)

        settings = BotFrameworkAdapterSettings(
            app_id="bot_id", credential_provider=mock_credential_provider
        )
        adapter = BotFrameworkAdapter(settings)

        skill_1_app_id = "00000000-0000-0000-0000-000000skill1"
        skill_2_app_id = "00000000-0000-0000-0000-000000skill2"

        skills_identity = ClaimsIdentity(
            claims={
                AuthenticationConstants.AUDIENCE_CLAIM: skill_1_app_id,
                AuthenticationConstants.APP_ID_CLAIM: skill_2_app_id,
                AuthenticationConstants.VERSION_CLAIM: "1.0",
            },
            is_authenticated=True,
        )

        skill_2_service_url = "https://skill2.com/api/skills/"

        async def callback(context: TurnContext):
            TestBotFrameworkAdapter.get_creds_and_assert_values(
                context, skill_1_app_id, skill_2_app_id, 1,
            )
            TestBotFrameworkAdapter.get_client_and_assert_values(
                context, skill_1_app_id, skill_2_app_id, skill_2_service_url, 1,
            )

            # pylint: disable=protected-access
            client_cache = context.adapter._connector_client_cache
            client = client_cache.get(
                BotFrameworkAdapter.key_for_connector_client(
                    skill_2_service_url, skill_1_app_id, skill_2_app_id,
                )
            )
            assert client

            turn_state_client = context.turn_state.get(
                BotFrameworkAdapter.BOT_CONNECTOR_CLIENT_KEY
            )
            assert turn_state_client
            client_creds = turn_state_client.config.credentials

            assert skill_1_app_id == client_creds.microsoft_app_id
            assert skill_2_app_id == client_creds.oauth_scope
            assert client.config.base_url == turn_state_client.config.base_url

            scope = context.turn_state[BotFrameworkAdapter.BOT_OAUTH_SCOPE_KEY]
            assert skill_2_app_id == scope

            # Ensure the serviceUrl was added to the trusted hosts
            assert AppCredentials.is_trusted_service(skill_2_service_url)

        refs = ConversationReference(service_url=skill_2_service_url)

        # Ensure the serviceUrl is NOT in the trusted hosts
        assert not AppCredentials.is_trusted_service(skill_2_service_url)

        await adapter.continue_conversation(
            refs, callback, claims_identity=skills_identity, audience=skill_2_app_id
        )

    async def test_delivery_mode_expect_replies(self):
        mock_credential_provider = unittest.mock.create_autospec(CredentialProvider)

        settings = BotFrameworkAdapterSettings(
            app_id="bot_id", credential_provider=mock_credential_provider
        )
        adapter = AdapterUnderTest(settings)

        async def callback(context: TurnContext):
            await context.send_activity("activity 1")
            await context.send_activity("activity 2")
            await context.send_activity("activity 3")

        inbound_activity = Activity(
            type=ActivityTypes.message,
            channel_id="emulator",
            service_url="http://tempuri.org/whatever",
            delivery_mode=DeliveryModes.expect_replies,
            text="hello world",
        )

        identity = ClaimsIdentity(
            claims={
                AuthenticationConstants.AUDIENCE_CLAIM: "bot_id",
                AuthenticationConstants.APP_ID_CLAIM: "bot_id",
                AuthenticationConstants.VERSION_CLAIM: "1.0",
            },
            is_authenticated=True,
        )

        invoke_response = await adapter.process_activity_with_identity(
            inbound_activity, identity, callback
        )
        assert invoke_response
        assert invoke_response.status == 200
        activities = ExpectedReplies().deserialize(invoke_response.body).activities
        assert len(activities) == 3
        assert activities[0].text == "activity 1"
        assert activities[1].text == "activity 2"
        assert activities[2].text == "activity 3"
        assert (
            adapter.connector_client_mock.conversations.send_to_conversation.call_count
            == 0
        )

    async def test_delivery_mode_normal(self):
        mock_credential_provider = unittest.mock.create_autospec(CredentialProvider)

        settings = BotFrameworkAdapterSettings(
            app_id="bot_id", credential_provider=mock_credential_provider
        )
        adapter = AdapterUnderTest(settings)

        async def callback(context: TurnContext):
            await context.send_activity("activity 1")
            await context.send_activity("activity 2")
            await context.send_activity("activity 3")

        inbound_activity = Activity(
            type=ActivityTypes.message,
            channel_id="emulator",
            service_url="http://tempuri.org/whatever",
            delivery_mode=DeliveryModes.normal,
            text="hello world",
            conversation=ConversationAccount(id="conversationId"),
        )

        identity = ClaimsIdentity(
            claims={
                AuthenticationConstants.AUDIENCE_CLAIM: "bot_id",
                AuthenticationConstants.APP_ID_CLAIM: "bot_id",
                AuthenticationConstants.VERSION_CLAIM: "1.0",
            },
            is_authenticated=True,
        )

        invoke_response = await adapter.process_activity_with_identity(
            inbound_activity, identity, callback
        )
        assert not invoke_response
        assert (
            adapter.connector_client_mock.conversations.send_to_conversation.call_count
            == 3
        )
