# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import uuid
from http import HTTPStatus
from typing import Callable, Union, List
from unittest.mock import Mock

import aiounittest
from botframework.connector.token_api.models import TokenExchangeResource
from botbuilder.core import (
    ConversationState,
    MemoryStorage,
    InvokeResponse,
    TurnContext,
    MessageFactory,
)
from botbuilder.core.card_factory import ContentTypes
from botbuilder.core.skills import (
    BotFrameworkSkill,
    ConversationIdFactoryBase,
    SkillConversationIdFactoryOptions,
    SkillConversationReference,
    BotFrameworkClient,
)
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ConversationReference,
    OAuthCard,
    Attachment,
    ConversationAccount,
    ChannelAccount,
    ExpectedReplies,
    DeliveryModes,
)
from botbuilder.testing import DialogTestClient

from botbuilder.dialogs import (
    SkillDialog,
    SkillDialogOptions,
    BeginSkillDialogOptions,
    DialogTurnStatus,
)


class SimpleConversationIdFactory(ConversationIdFactoryBase):
    def __init__(self):
        self.conversation_refs = {}
        self.create_count = 0

    async def create_skill_conversation_id(
        self,
        options_or_conversation_reference: Union[
            SkillConversationIdFactoryOptions, ConversationReference
        ],
    ) -> str:
        self.create_count += 1
        key = (
            options_or_conversation_reference.activity.conversation.id
            + options_or_conversation_reference.activity.service_url
        )
        if key not in self.conversation_refs:
            self.conversation_refs[key] = SkillConversationReference(
                conversation_reference=TurnContext.get_conversation_reference(
                    options_or_conversation_reference.activity
                ),
                oauth_scope=options_or_conversation_reference.from_bot_oauth_scope,
            )
        return key

    async def get_conversation_reference(
        self, skill_conversation_id: str
    ) -> Union[SkillConversationReference, ConversationReference]:
        return self.conversation_refs[skill_conversation_id]

    async def delete_conversation_reference(self, skill_conversation_id: str):
        self.conversation_refs.pop(skill_conversation_id, None)
        return


class SkillDialogTests(aiounittest.AsyncTestCase):
    async def test_constructor_validation_test(self):
        # missing dialog_id
        with self.assertRaises(TypeError):
            SkillDialog(SkillDialogOptions(), None)

        # missing dialog options
        with self.assertRaises(TypeError):
            SkillDialog(None, "dialog_id")

    async def test_begin_dialog_options_validation(self):
        dialog_options = SkillDialogOptions()
        sut = SkillDialog(dialog_options, dialog_id="dialog_id")

        # empty options should raise
        client = DialogTestClient("test", sut)
        with self.assertRaises(TypeError):
            await client.send_activity("irrelevant")

        # non DialogArgs should raise
        client = DialogTestClient("test", sut, {})
        with self.assertRaises(TypeError):
            await client.send_activity("irrelevant")

        # Activity in DialogArgs should be set
        client = DialogTestClient("test", sut, BeginSkillDialogOptions(None))
        with self.assertRaises(TypeError):
            await client.send_activity("irrelevant")

    async def test_begin_dialog_calls_skill_no_deliverymode(self):
        return await self.begin_dialog_calls_skill(None)

    async def test_begin_dialog_calls_skill_expect_replies(self):
        return await self.begin_dialog_calls_skill(DeliveryModes.expect_replies)

    async def begin_dialog_calls_skill(self, deliver_mode: str):
        activity_sent = None
        from_bot_id_sent = None
        to_bot_id_sent = None
        to_url_sent = None

        async def capture(
            from_bot_id: str,
            to_bot_id: str,
            to_url: str,
            service_url: str,  # pylint: disable=unused-argument
            conversation_id: str,  # pylint: disable=unused-argument
            activity: Activity,
        ):
            nonlocal from_bot_id_sent, to_bot_id_sent, to_url_sent, activity_sent
            from_bot_id_sent = from_bot_id
            to_bot_id_sent = to_bot_id
            to_url_sent = to_url
            activity_sent = activity

        mock_skill_client = self._create_mock_skill_client(capture)

        conversation_state = ConversationState(MemoryStorage())
        dialog_options = SkillDialogTests.create_skill_dialog_options(
            conversation_state, mock_skill_client
        )

        sut = SkillDialog(dialog_options, "dialog_id")
        activity_to_send = MessageFactory.text(str(uuid.uuid4()))
        activity_to_send.delivery_mode = deliver_mode

        client = DialogTestClient(
            "test",
            sut,
            BeginSkillDialogOptions(activity=activity_to_send),
            conversation_state=conversation_state,
        )

        assert len(dialog_options.conversation_id_factory.conversation_refs) == 0

        # Send something to the dialog to start it
        await client.send_activity(MessageFactory.text("irrelevant"))

        # Assert results and data sent to the SkillClient for fist turn
        assert len(dialog_options.conversation_id_factory.conversation_refs) == 1
        assert dialog_options.bot_id == from_bot_id_sent
        assert dialog_options.skill.app_id == to_bot_id_sent
        assert dialog_options.skill.skill_endpoint == to_url_sent
        assert activity_to_send.text == activity_sent.text
        assert DialogTurnStatus.Waiting == client.dialog_turn_result.status

        # Send a second message to continue the dialog
        await client.send_activity(MessageFactory.text("Second message"))

        # Assert results for second turn
        assert len(dialog_options.conversation_id_factory.conversation_refs) == 1
        assert activity_sent.text == "Second message"
        assert DialogTurnStatus.Waiting == client.dialog_turn_result.status

        # Send EndOfConversation to the dialog
        await client.send_activity(Activity(type=ActivityTypes.end_of_conversation))

        # Assert we are done.
        assert DialogTurnStatus.Complete == client.dialog_turn_result.status

    async def test_should_handle_invoke_activities(self):
        activity_sent = None
        from_bot_id_sent = None
        to_bot_id_sent = None
        to_url_sent = None

        async def capture(
            from_bot_id: str,
            to_bot_id: str,
            to_url: str,
            service_url: str,  # pylint: disable=unused-argument
            conversation_id: str,  # pylint: disable=unused-argument
            activity: Activity,
        ):
            nonlocal from_bot_id_sent, to_bot_id_sent, to_url_sent, activity_sent
            from_bot_id_sent = from_bot_id
            to_bot_id_sent = to_bot_id
            to_url_sent = to_url
            activity_sent = activity

        mock_skill_client = self._create_mock_skill_client(capture)

        conversation_state = ConversationState(MemoryStorage())
        dialog_options = SkillDialogTests.create_skill_dialog_options(
            conversation_state, mock_skill_client
        )

        sut = SkillDialog(dialog_options, "dialog_id")
        activity_to_send = Activity(type=ActivityTypes.invoke, name=str(uuid.uuid4()),)

        client = DialogTestClient(
            "test",
            sut,
            BeginSkillDialogOptions(activity=activity_to_send),
            conversation_state=conversation_state,
        )

        # Send something to the dialog to start it
        await client.send_activity(MessageFactory.text("irrelevant"))

        # Assert results and data sent to the SkillClient for fist turn
        assert dialog_options.bot_id == from_bot_id_sent
        assert dialog_options.skill.app_id == to_bot_id_sent
        assert dialog_options.skill.skill_endpoint == to_url_sent
        assert activity_to_send.text == activity_sent.text
        assert DialogTurnStatus.Waiting == client.dialog_turn_result.status

        # Send a second message to continue the dialog
        await client.send_activity(MessageFactory.text("Second message"))

        # Assert results for second turn
        assert activity_sent.text == "Second message"
        assert DialogTurnStatus.Waiting == client.dialog_turn_result.status

        # Send EndOfConversation to the dialog
        await client.send_activity(Activity(type=ActivityTypes.end_of_conversation))

        # Assert we are done.
        assert DialogTurnStatus.Complete == client.dialog_turn_result.status

    async def test_cancel_dialog_sends_eoc(self):
        activity_sent = None

        async def capture(
            from_bot_id: str,  # pylint: disable=unused-argument
            to_bot_id: str,  # pylint: disable=unused-argument
            to_url: str,  # pylint: disable=unused-argument
            service_url: str,  # pylint: disable=unused-argument
            conversation_id: str,  # pylint: disable=unused-argument
            activity: Activity,
        ):
            nonlocal activity_sent
            activity_sent = activity

        mock_skill_client = self._create_mock_skill_client(capture)

        conversation_state = ConversationState(MemoryStorage())
        dialog_options = SkillDialogTests.create_skill_dialog_options(
            conversation_state, mock_skill_client
        )

        sut = SkillDialog(dialog_options, "dialog_id")
        activity_to_send = MessageFactory.text(str(uuid.uuid4()))

        client = DialogTestClient(
            "test",
            sut,
            BeginSkillDialogOptions(activity=activity_to_send),
            conversation_state=conversation_state,
        )

        # Send something to the dialog to start it
        await client.send_activity(MessageFactory.text("irrelevant"))

        # Cancel the dialog so it sends an EoC to the skill
        await client.dialog_context.cancel_all_dialogs()

        assert activity_sent
        assert activity_sent.type == ActivityTypes.end_of_conversation

    async def test_should_throw_on_post_failure(self):
        # This mock client will fail
        mock_skill_client = self._create_mock_skill_client(None, 500)

        conversation_state = ConversationState(MemoryStorage())
        dialog_options = SkillDialogTests.create_skill_dialog_options(
            conversation_state, mock_skill_client
        )

        sut = SkillDialog(dialog_options, "dialog_id")
        activity_to_send = MessageFactory.text(str(uuid.uuid4()))

        client = DialogTestClient(
            "test",
            sut,
            BeginSkillDialogOptions(activity=activity_to_send),
            conversation_state=conversation_state,
        )

        # A send should raise an exception
        with self.assertRaises(Exception):
            await client.send_activity("irrelevant")

    async def test_should_intercept_oauth_cards_for_sso(self):
        connection_name = "connectionName"
        first_response = ExpectedReplies(
            activities=[
                SkillDialogTests.create_oauth_card_attachment_activity("https://test")
            ]
        )

        sequence = 0

        async def post_return():
            nonlocal sequence
            if sequence == 0:
                result = InvokeResponse(body=first_response, status=HTTPStatus.OK)
            else:
                result = InvokeResponse(status=HTTPStatus.OK)
            sequence += 1
            return result

        mock_skill_client = self._create_mock_skill_client(None, post_return)
        conversation_state = ConversationState(MemoryStorage())

        dialog_options = SkillDialogTests.create_skill_dialog_options(
            conversation_state, mock_skill_client, connection_name
        )
        sut = SkillDialog(dialog_options, dialog_id="dialog")
        activity_to_send = SkillDialogTests.create_send_activity()

        client = DialogTestClient(
            "test",
            sut,
            BeginSkillDialogOptions(activity=activity_to_send,),
            conversation_state=conversation_state,
        )

        client.test_adapter.add_exchangeable_token(
            connection_name, "test", "User1", "https://test", "https://test1"
        )

        final_activity = await client.send_activity(MessageFactory.text("irrelevant"))
        self.assertIsNone(final_activity)

    async def test_should_not_intercept_oauth_cards_for_empty_connection_name(self):
        connection_name = "connectionName"
        first_response = ExpectedReplies(
            activities=[
                SkillDialogTests.create_oauth_card_attachment_activity("https://test")
            ]
        )

        sequence = 0

        async def post_return():
            nonlocal sequence
            if sequence == 0:
                result = InvokeResponse(body=first_response, status=HTTPStatus.OK)
            else:
                result = InvokeResponse(status=HTTPStatus.OK)
            sequence += 1
            return result

        mock_skill_client = self._create_mock_skill_client(None, post_return)
        conversation_state = ConversationState(MemoryStorage())

        dialog_options = SkillDialogTests.create_skill_dialog_options(
            conversation_state, mock_skill_client
        )
        sut = SkillDialog(dialog_options, dialog_id="dialog")
        activity_to_send = SkillDialogTests.create_send_activity()

        client = DialogTestClient(
            "test",
            sut,
            BeginSkillDialogOptions(activity=activity_to_send,),
            conversation_state=conversation_state,
        )

        client.test_adapter.add_exchangeable_token(
            connection_name, "test", "User1", "https://test", "https://test1"
        )

        final_activity = await client.send_activity(MessageFactory.text("irrelevant"))
        self.assertIsNotNone(final_activity)
        self.assertEqual(len(final_activity.attachments), 1)

    async def test_should_not_intercept_oauth_cards_for_empty_token(self):
        first_response = ExpectedReplies(
            activities=[
                SkillDialogTests.create_oauth_card_attachment_activity("https://test")
            ]
        )

        sequence = 0

        async def post_return():
            nonlocal sequence
            if sequence == 0:
                result = InvokeResponse(body=first_response, status=HTTPStatus.OK)
            else:
                result = InvokeResponse(status=HTTPStatus.OK)
            sequence += 1
            return result

        mock_skill_client = self._create_mock_skill_client(None, post_return)
        conversation_state = ConversationState(MemoryStorage())

        dialog_options = SkillDialogTests.create_skill_dialog_options(
            conversation_state, mock_skill_client
        )
        sut = SkillDialog(dialog_options, dialog_id="dialog")
        activity_to_send = SkillDialogTests.create_send_activity()

        client = DialogTestClient(
            "test",
            sut,
            BeginSkillDialogOptions(activity=activity_to_send,),
            conversation_state=conversation_state,
        )

        # Don't add exchangeable token to test adapter

        final_activity = await client.send_activity(MessageFactory.text("irrelevant"))
        self.assertIsNotNone(final_activity)
        self.assertEqual(len(final_activity.attachments), 1)

    async def test_should_not_intercept_oauth_cards_for_token_exception(self):
        connection_name = "connectionName"
        first_response = ExpectedReplies(
            activities=[
                SkillDialogTests.create_oauth_card_attachment_activity("https://test")
            ]
        )

        sequence = 0

        async def post_return():
            nonlocal sequence
            if sequence == 0:
                result = InvokeResponse(body=first_response, status=HTTPStatus.OK)
            else:
                result = InvokeResponse(status=HTTPStatus.OK)
            sequence += 1
            return result

        mock_skill_client = self._create_mock_skill_client(None, post_return)
        conversation_state = ConversationState(MemoryStorage())

        dialog_options = SkillDialogTests.create_skill_dialog_options(
            conversation_state, mock_skill_client, connection_name
        )
        sut = SkillDialog(dialog_options, dialog_id="dialog")
        activity_to_send = SkillDialogTests.create_send_activity()
        initial_dialog_options = BeginSkillDialogOptions(activity=activity_to_send,)

        client = DialogTestClient(
            "test", sut, initial_dialog_options, conversation_state=conversation_state,
        )
        client.test_adapter.throw_on_exchange_request(
            connection_name, "test", "User1", "https://test"
        )

        final_activity = await client.send_activity(MessageFactory.text("irrelevant"))
        self.assertIsNotNone(final_activity)
        self.assertEqual(len(final_activity.attachments), 1)

    async def test_should_not_intercept_oauth_cards_for_bad_request(self):
        connection_name = "connectionName"
        first_response = ExpectedReplies(
            activities=[
                SkillDialogTests.create_oauth_card_attachment_activity("https://test")
            ]
        )

        sequence = 0

        async def post_return():
            nonlocal sequence
            if sequence == 0:
                result = InvokeResponse(body=first_response, status=HTTPStatus.OK)
            else:
                result = InvokeResponse(status=HTTPStatus.CONFLICT)
            sequence += 1
            return result

        mock_skill_client = self._create_mock_skill_client(None, post_return)
        conversation_state = ConversationState(MemoryStorage())

        dialog_options = SkillDialogTests.create_skill_dialog_options(
            conversation_state, mock_skill_client, connection_name
        )
        sut = SkillDialog(dialog_options, dialog_id="dialog")
        activity_to_send = SkillDialogTests.create_send_activity()

        client = DialogTestClient(
            "test",
            sut,
            BeginSkillDialogOptions(activity=activity_to_send,),
            conversation_state=conversation_state,
        )

        client.test_adapter.add_exchangeable_token(
            connection_name, "test", "User1", "https://test", "https://test1"
        )

        final_activity = await client.send_activity(MessageFactory.text("irrelevant"))
        self.assertIsNotNone(final_activity)
        self.assertEqual(len(final_activity.attachments), 1)

    async def test_end_of_conversation_from_expect_replies_calls_delete_conversation_reference(
        self,
    ):
        activity_sent: Activity = None

        # Callback to capture the parameters sent to the skill
        async def capture_action(
            from_bot_id: str,  # pylint: disable=unused-argument
            to_bot_id: str,  # pylint: disable=unused-argument
            to_uri: str,  # pylint: disable=unused-argument
            service_url: str,  # pylint: disable=unused-argument
            conversation_id: str,  # pylint: disable=unused-argument
            activity: Activity,
        ):
            # Capture values sent to the skill so we can assert the right parameters were used.
            nonlocal activity_sent
            activity_sent = activity

        eoc = Activity.create_end_of_conversation_activity()
        expected_replies = list([eoc])

        # Create a mock skill client to intercept calls and capture what is sent.
        mock_skill_client = self._create_mock_skill_client(
            capture_action, expected_replies=expected_replies
        )

        # Use Memory for conversation state
        conversation_state = ConversationState(MemoryStorage())
        dialog_options = self.create_skill_dialog_options(
            conversation_state, mock_skill_client
        )

        # Create the SkillDialogInstance and the activity to send.
        sut = SkillDialog(dialog_options, dialog_id="dialog")
        activity_to_send = Activity.create_message_activity()
        activity_to_send.delivery_mode = DeliveryModes.expect_replies
        activity_to_send.text = str(uuid.uuid4())
        client = DialogTestClient(
            "test",
            sut,
            BeginSkillDialogOptions(activity_to_send),
            conversation_state=conversation_state,
        )

        # Send something to the dialog to start it
        await client.send_activity("hello")

        simple_id_factory: SimpleConversationIdFactory = dialog_options.conversation_id_factory
        self.assertEqual(0, len(simple_id_factory.conversation_refs))
        self.assertEqual(1, simple_id_factory.create_count)

    @staticmethod
    def create_skill_dialog_options(
        conversation_state: ConversationState,
        skill_client: BotFrameworkClient,
        connection_name: str = None,
    ):
        return SkillDialogOptions(
            bot_id=str(uuid.uuid4()),
            skill_host_endpoint="http://test.contoso.com/skill/messages",
            conversation_id_factory=SimpleConversationIdFactory(),
            conversation_state=conversation_state,
            skill_client=skill_client,
            skill=BotFrameworkSkill(
                app_id=str(uuid.uuid4()),
                skill_endpoint="http://testskill.contoso.com/api/messages",
            ),
            connection_name=connection_name,
        )

    @staticmethod
    def create_send_activity() -> Activity:
        return Activity(
            type=ActivityTypes.message,
            delivery_mode=DeliveryModes.expect_replies,
            text=str(uuid.uuid4()),
        )

    @staticmethod
    def create_oauth_card_attachment_activity(uri: str) -> Activity:
        oauth_card = OAuthCard(token_exchange_resource=TokenExchangeResource(uri=uri))
        attachment = Attachment(
            content_type=ContentTypes.oauth_card, content=oauth_card,
        )

        attachment_activity = MessageFactory.attachment(attachment)
        attachment_activity.conversation = ConversationAccount(id=str(uuid.uuid4()))
        attachment_activity.from_property = ChannelAccount(id="blah", name="name")

        return attachment_activity

    def _create_mock_skill_client(
        self,
        callback: Callable,
        return_status: Union[Callable, int] = 200,
        expected_replies: List[Activity] = None,
    ) -> BotFrameworkClient:
        mock_client = Mock()
        activity_list = ExpectedReplies(
            activities=expected_replies or [MessageFactory.text("dummy activity")]
        )

        async def mock_post_activity(
            from_bot_id: str,
            to_bot_id: str,
            to_url: str,
            service_url: str,
            conversation_id: str,
            activity: Activity,
        ):
            nonlocal callback, return_status
            if callback:
                await callback(
                    from_bot_id,
                    to_bot_id,
                    to_url,
                    service_url,
                    conversation_id,
                    activity,
                )

            if isinstance(return_status, Callable):
                return await return_status()
            return InvokeResponse(status=return_status, body=activity_list)

        mock_client.post_activity.side_effect = mock_post_activity

        return mock_client
