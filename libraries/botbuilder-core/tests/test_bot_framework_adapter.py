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
)
from botframework.connector.aio import ConnectorClient
from botframework.connector.auth import ClaimsIdentity

REFERENCE = ConversationReference(
    activity_id="1234",
    channel_id="test",
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

    def aux_test_authenticate_request(self, request: Activity, auth_header: str):
        return super().authenticate_request(request, auth_header)

    async def aux_test_create_connector_client(self, service_url: str):
        return await super().create_connector_client(service_url)

    async def authenticate_request(self, request: Activity, auth_header: str):
        self.tester.assertIsNotNone(
            request, "authenticate_request() not passed request."
        )
        self.tester.assertEqual(
            auth_header,
            self.expect_auth_header,
            "authenticateRequest() not passed expected authHeader.",
        )
        return not self.fail_auth

    async def create_connector_client(
        self,
        service_url: str,
        identity: ClaimsIdentity = None,  # pylint: disable=unused-argument
    ) -> ConnectorClient:
        self.tester.assertIsNotNone(
            service_url, "create_connector_client() not passed service_url."
        )
        connector_client_mock = Mock()

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

        connector_client_mock.conversations.reply_to_activity.side_effect = (
            mock_reply_to_activity
        )
        connector_client_mock.conversations.send_to_conversation.side_effect = (
            mock_send_to_conversation
        )
        connector_client_mock.conversations.update_activity.side_effect = (
            mock_update_activity
        )
        connector_client_mock.conversations.delete_activity.side_effect = (
            mock_delete_activity
        )
        connector_client_mock.conversations.create_conversation.side_effect = (
            mock_create_conversation
        )

        return connector_client_mock


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

    async def test_should_update_activity(self):
        adapter = AdapterUnderTest()
        context = TurnContext(adapter, INCOMING_MESSAGE)
        self.assertTrue(
            await adapter.update_activity(context, INCOMING_MESSAGE),
            "Activity not updated.",
        )

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
                context.activity.channel_data["tenant"]["id"],
                tenant_id,
                "request has invalid tenant_id in channel_data",
            )
            nonlocal called
            called = True

        await adapter.create_conversation(reference, aux_func_assert_valid_conversation)
        self.assertTrue(called, "bot logic not called.")
