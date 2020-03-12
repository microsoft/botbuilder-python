# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import uuid
from typing import Callable, Union
from unittest.mock import Mock

import aiounittest
from botbuilder.core import (
    ConversationState,
    MemoryStorage,
    InvokeResponse,
    TurnContext,
    MessageFactory,
)
from botbuilder.core.skills import (
    BotFrameworkSkill,
    ConversationIdFactoryBase,
    SkillConversationIdFactoryOptions,
    SkillConversationReference,
    BotFrameworkClient,
)
from botbuilder.schema import Activity, ActivityTypes, ConversationReference
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

    async def create_skill_conversation_id(
        self,
        options_or_conversation_reference: Union[
            SkillConversationIdFactoryOptions, ConversationReference
        ],
    ) -> str:
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
        raise NotImplementedError()


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

        # Only Message and Event activities are supported
        client = DialogTestClient(
            "test",
            sut,
            BeginSkillDialogOptions(Activity(type=ActivityTypes.conversation_update)),
        )
        with self.assertRaises(TypeError):
            await client.send_activity("irrelevant")

    async def test_begin_dialog_calls_skill(self):
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
        dialog_options = self._create_skill_dialog_options(
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

        await client.send_activity(MessageFactory.text("irrelevant"))

        assert dialog_options.bot_id == from_bot_id_sent
        assert dialog_options.skill.app_id == to_bot_id_sent
        assert dialog_options.skill.skill_endpoint == to_url_sent
        assert activity_to_send.text == activity_sent.text
        assert DialogTurnStatus.Waiting == client.dialog_turn_result.status

        await client.send_activity(MessageFactory.text("Second message"))

        assert activity_sent.text == "Second message"
        assert DialogTurnStatus.Waiting == client.dialog_turn_result.status

        await client.send_activity(Activity(type=ActivityTypes.end_of_conversation))

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
        dialog_options = self._create_skill_dialog_options(
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
        dialog_options = self._create_skill_dialog_options(
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

    def _create_skill_dialog_options(
        self, conversation_state: ConversationState, skill_client: BotFrameworkClient
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
        )

    def _create_mock_skill_client(
        self, callback: Callable, return_status: int = 200
    ) -> BotFrameworkClient:
        mock_client = Mock()

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
            return InvokeResponse(status=return_status)

        mock_client.post_activity.side_effect = mock_post_activity

        return mock_client
