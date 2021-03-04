# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest

from botframework.connector.auth import MicrosoftAppCredentials
from botbuilder.core import TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import Activity, ConversationReference, ChannelAccount

RECEIVED_MESSAGE = Activity(type="message", text="received")
UPDATED_ACTIVITY = Activity(type="message", text="update")
DELETED_ACTIVITY_REFERENCE = ConversationReference(activity_id="1234")


class TestTestAdapter(aiounittest.AsyncTestCase):
    async def test_should_call_bog_logic_when_receive_activity_is_called(self):
        async def logic(context: TurnContext):
            assert context
            assert context.activity
            assert context.activity.type == "message"
            assert context.activity.text == "test"
            assert context.activity.id
            assert context.activity.from_property
            assert context.activity.recipient
            assert context.activity.conversation
            assert context.activity.channel_id
            assert context.activity.service_url

        adapter = TestAdapter(logic)
        await adapter.receive_activity("test")

    async def test_should_support_receive_activity_with_activity(self):
        async def logic(context: TurnContext):
            assert context.activity.type == "message"
            assert context.activity.text == "test"

        adapter = TestAdapter(logic)
        await adapter.receive_activity(Activity(type="message", text="test"))

    async def test_should_set_activity_type_when_receive_activity_receives_activity_without_type(
        self,
    ):
        async def logic(context: TurnContext):
            assert context.activity.type == "message"
            assert context.activity.text == "test"

        adapter = TestAdapter(logic)
        await adapter.receive_activity(Activity(text="test"))

    async def test_should_support_custom_activity_id_in_receive_activity(self):
        async def logic(context: TurnContext):
            assert context.activity.id == "myId"
            assert context.activity.type == "message"
            assert context.activity.text == "test"

        adapter = TestAdapter(logic)
        await adapter.receive_activity(Activity(type="message", text="test", id="myId"))

    async def test_should_call_bot_logic_when_send_is_called(self):
        async def logic(context: TurnContext):
            assert context.activity.text == "test"

        adapter = TestAdapter(logic)
        await adapter.send("test")

    async def test_should_send_and_receive_when_test_is_called(self):
        async def logic(context: TurnContext):
            await context.send_activity(RECEIVED_MESSAGE)

        adapter = TestAdapter(logic)
        await adapter.test("test", "received")

    async def test_should_send_and_throw_assertion_error_when_test_is_called(self):
        async def logic(context: TurnContext):
            await context.send_activity(RECEIVED_MESSAGE)

        adapter = TestAdapter(logic)
        try:
            await adapter.test("test", "foobar")
        except AssertionError:
            pass
        else:
            raise AssertionError("Assertion error should have been raised")

    async def test_tests_should_call_test_for_each_tuple(self):
        counter = 0

        async def logic(context: TurnContext):
            nonlocal counter
            counter += 1
            await context.send_activity(Activity(type="message", text=str(counter)))

        adapter = TestAdapter(logic)
        await adapter.tests(("test", "1"), ("test", "2"), ("test", "3"))
        assert counter == 3

    async def test_tests_should_call_test_for_each_list(self):
        counter = 0

        async def logic(context: TurnContext):
            nonlocal counter
            counter += 1
            await context.send_activity(Activity(type="message", text=str(counter)))

        adapter = TestAdapter(logic)
        await adapter.tests(["test", "1"], ["test", "2"], ["test", "3"])
        assert counter == 3

    async def test_should_assert_reply_after_send(self):
        async def logic(context: TurnContext):
            await context.send_activity(RECEIVED_MESSAGE)

        adapter = TestAdapter(logic)
        test_flow = await adapter.send("test")
        await test_flow.assert_reply("received")

    async def test_should_support_context_update_activity_call(self):
        async def logic(context: TurnContext):
            await context.update_activity(UPDATED_ACTIVITY)
            await context.send_activity(RECEIVED_MESSAGE)

        adapter = TestAdapter(logic)
        await adapter.test("test", "received")
        assert len(adapter.updated_activities) == 1
        assert adapter.updated_activities[0].text == UPDATED_ACTIVITY.text

    async def test_should_support_context_delete_activity_call(self):
        async def logic(context: TurnContext):
            await context.delete_activity(DELETED_ACTIVITY_REFERENCE)
            await context.send_activity(RECEIVED_MESSAGE)

        adapter = TestAdapter(logic)
        await adapter.test("test", "received")
        assert len(adapter.deleted_activities) == 1
        assert (
            adapter.deleted_activities[0].activity_id
            == DELETED_ACTIVITY_REFERENCE.activity_id
        )

    async def test_get_user_token_returns_null(self):
        adapter = TestAdapter()
        activity = Activity(
            channel_id="directline", from_property=ChannelAccount(id="testuser")
        )

        turn_context = TurnContext(adapter, activity)

        token_response = await adapter.get_user_token(turn_context, "myConnection")
        assert not token_response

        oauth_app_credentials = MicrosoftAppCredentials(None, None)
        token_response = await adapter.get_user_token(
            turn_context, "myConnection", oauth_app_credentials=oauth_app_credentials
        )
        assert not token_response

    async def test_get_user_token_returns_null_with_code(self):
        adapter = TestAdapter()
        activity = Activity(
            channel_id="directline", from_property=ChannelAccount(id="testuser")
        )

        turn_context = TurnContext(adapter, activity)

        token_response = await adapter.get_user_token(
            turn_context, "myConnection", "abc123"
        )
        assert not token_response

        oauth_app_credentials = MicrosoftAppCredentials(None, None)
        token_response = await adapter.get_user_token(
            turn_context,
            "myConnection",
            "abc123",
            oauth_app_credentials=oauth_app_credentials,
        )
        assert not token_response

    async def test_get_user_token_returns_token(self):
        adapter = TestAdapter()
        connection_name = "myConnection"
        channel_id = "directline"
        user_id = "testUser"
        token = "abc123"
        activity = Activity(
            channel_id=channel_id, from_property=ChannelAccount(id=user_id)
        )

        turn_context = TurnContext(adapter, activity)

        adapter.add_user_token(connection_name, channel_id, user_id, token)

        token_response = await adapter.get_user_token(turn_context, connection_name)
        assert token_response
        assert token == token_response.token
        assert connection_name == token_response.connection_name

        oauth_app_credentials = MicrosoftAppCredentials(None, None)
        token_response = await adapter.get_user_token(
            turn_context, connection_name, oauth_app_credentials=oauth_app_credentials
        )
        assert token_response
        assert token == token_response.token
        assert connection_name == token_response.connection_name

    async def test_get_user_token_returns_token_with_magice_code(self):
        adapter = TestAdapter()
        connection_name = "myConnection"
        channel_id = "directline"
        user_id = "testUser"
        token = "abc123"
        magic_code = "888999"
        activity = Activity(
            channel_id=channel_id, from_property=ChannelAccount(id=user_id)
        )

        turn_context = TurnContext(adapter, activity)

        adapter.add_user_token(connection_name, channel_id, user_id, token, magic_code)

        # First no magic_code
        token_response = await adapter.get_user_token(turn_context, connection_name)
        assert not token_response

        # Can be retrieved with magic code
        token_response = await adapter.get_user_token(
            turn_context, connection_name, magic_code
        )
        assert token_response
        assert token == token_response.token
        assert connection_name == token_response.connection_name

        # Then can be retrieved without magic code
        token_response = await adapter.get_user_token(turn_context, connection_name)
        assert token_response
        assert token == token_response.token
        assert connection_name == token_response.connection_name

        # Then can be retrieved using customized AppCredentials
        oauth_app_credentials = MicrosoftAppCredentials(None, None)
        token_response = await adapter.get_user_token(
            turn_context, connection_name, oauth_app_credentials=oauth_app_credentials
        )
        assert token_response
        assert token == token_response.token
        assert connection_name == token_response.connection_name

    async def test_should_validate_no_reply_when_no_reply_expected(self):
        async def logic(context: TurnContext):
            await context.send_activity(RECEIVED_MESSAGE)

        adapter = TestAdapter(logic)
        test_flow = await adapter.test("test", "received")
        await test_flow.assert_no_reply("should be no additional replies")

    async def test_should_timeout_waiting_for_assert_no_reply_when_no_reply_expected(
        self,
    ):
        async def logic(context: TurnContext):
            await context.send_activity(RECEIVED_MESSAGE)

        adapter = TestAdapter(logic)
        test_flow = await adapter.test("test", "received")
        await test_flow.assert_no_reply("no reply received", 500)

    async def test_should_throw_error_with_assert_no_reply_when_no_reply_expected_but_was_received(
        self,
    ):
        async def logic(context: TurnContext):
            activities = [RECEIVED_MESSAGE, RECEIVED_MESSAGE]
            await context.send_activities(activities)

        adapter = TestAdapter(logic)
        test_flow = await adapter.test("test", "received")

        with self.assertRaises(Exception):
            await test_flow.assert_no_reply("should be no additional replies")
