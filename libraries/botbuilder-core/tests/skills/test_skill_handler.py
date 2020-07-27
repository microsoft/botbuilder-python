import hashlib
import json
from uuid import uuid4
from asyncio import Future
from typing import Dict, List

from unittest.mock import Mock, MagicMock
import aiounittest

from botbuilder.core import (
    TurnContext,
    BotActionNotImplementedError,
    conversation_reference_extension,
)
from botbuilder.core.skills import ConversationIdFactoryBase, SkillHandler
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    AttachmentData,
    ChannelAccount,
    ConversationAccount,
    ConversationParameters,
    ConversationsResult,
    ConversationResourceResponse,
    ConversationReference,
    PagedMembersResult,
    ResourceResponse,
    Transcript,
    CallerIdConstants,
)
from botframework.connector.auth import (
    AuthenticationConfiguration,
    AuthenticationConstants,
    ClaimsIdentity,
)


class ConversationIdFactoryForTest(ConversationIdFactoryBase):
    def __init__(self):
        self._conversation_refs: Dict[str, str] = {}

    async def create_skill_conversation_id(  # pylint: disable=W0221
        self, conversation_reference: ConversationReference
    ) -> str:
        cr_json = json.dumps(conversation_reference.serialize())

        key = hashlib.md5(
            f"{conversation_reference.conversation.id}{conversation_reference.service_url}".encode()
        ).hexdigest()

        if key not in self._conversation_refs:
            self._conversation_refs[key] = cr_json

        return key

    async def get_conversation_reference(
        self, skill_conversation_id: str
    ) -> ConversationReference:
        conversation_reference = ConversationReference().deserialize(
            json.loads(self._conversation_refs[skill_conversation_id])
        )
        return conversation_reference

    async def delete_conversation_reference(self, skill_conversation_id: str):
        pass


class SkillHandlerInstanceForTests(SkillHandler):
    async def test_on_get_conversations(
        self, claims_identity: ClaimsIdentity, continuation_token: str = "",
    ) -> ConversationsResult:
        return await self.on_get_conversations(claims_identity, continuation_token)

    async def test_on_create_conversation(
        self, claims_identity: ClaimsIdentity, parameters: ConversationParameters,
    ) -> ConversationResourceResponse:
        return await self.on_create_conversation(claims_identity, parameters)

    async def test_on_send_to_conversation(
        self, claims_identity: ClaimsIdentity, conversation_id: str, activity: Activity,
    ) -> ResourceResponse:
        return await self.on_send_to_conversation(
            claims_identity, conversation_id, activity
        )

    async def test_on_send_conversation_history(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        transcript: Transcript,
    ) -> ResourceResponse:
        return await self.on_send_conversation_history(
            claims_identity, conversation_id, transcript
        )

    async def test_on_update_activity(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity_id: str,
        activity: Activity,
    ) -> ResourceResponse:
        return await self.on_update_activity(
            claims_identity, conversation_id, activity_id, activity
        )

    async def test_on_reply_to_activity(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity_id: str,
        activity: Activity,
    ) -> ResourceResponse:
        return await self.on_reply_to_activity(
            claims_identity, conversation_id, activity_id, activity
        )

    async def test_on_delete_activity(
        self, claims_identity: ClaimsIdentity, conversation_id: str, activity_id: str,
    ):
        return await self.on_delete_activity(
            claims_identity, conversation_id, activity_id
        )

    async def test_on_get_conversation_members(
        self, claims_identity: ClaimsIdentity, conversation_id: str,
    ) -> List[ChannelAccount]:
        return await self.on_get_conversation_members(claims_identity, conversation_id)

    async def test_on_get_conversation_paged_members(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        page_size: int = None,
        continuation_token: str = "",
    ) -> PagedMembersResult:
        return await self.on_get_conversation_paged_members(
            claims_identity, conversation_id, page_size, continuation_token
        )

    async def test_on_delete_conversation_member(
        self, claims_identity: ClaimsIdentity, conversation_id: str, member_id: str,
    ):
        return await self.on_delete_conversation_member(
            claims_identity, conversation_id, member_id
        )

    async def test_on_get_activity_members(
        self, claims_identity: ClaimsIdentity, conversation_id: str, activity_id: str,
    ) -> List[ChannelAccount]:
        return await self.on_get_activity_members(
            claims_identity, conversation_id, activity_id
        )

    async def test_on_upload_attachment(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        attachment_upload: AttachmentData,
    ) -> ResourceResponse:
        return await self.on_upload_attachment(
            claims_identity, conversation_id, attachment_upload
        )


# pylint: disable=invalid-name
# pylint: disable=attribute-defined-outside-init


class TestSkillHandler(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot_id = str(uuid4())
        cls.skill_id = str(uuid4())

        cls._test_id_factory = ConversationIdFactoryForTest()

        cls._claims_identity = ClaimsIdentity({}, False)

        cls._claims_identity.claims[AuthenticationConstants.AUDIENCE_CLAIM] = cls.bot_id
        cls._claims_identity.claims[AuthenticationConstants.APP_ID_CLAIM] = cls.skill_id
        cls._claims_identity.claims[
            AuthenticationConstants.SERVICE_URL_CLAIM
        ] = "http://testbot.com/api/messages"
        cls._conversation_reference = ConversationReference(
            conversation=ConversationAccount(id=str(uuid4())),
            service_url="http://testbot.com/api/messages",
        )

    def create_skill_handler_for_testing(self, adapter) -> SkillHandlerInstanceForTests:
        mock_bot = Mock()
        mock_bot.on_turn = MagicMock(return_value=Future())
        mock_bot.on_turn.return_value.set_result(Mock())

        return SkillHandlerInstanceForTests(
            adapter,
            mock_bot,
            self._test_id_factory,
            Mock(),
            AuthenticationConfiguration(),
        )

    async def test_on_send_to_conversation(self):
        self._conversation_id = await self._test_id_factory.create_skill_conversation_id(
            self._conversation_reference
        )

        mock_adapter = Mock()
        mock_adapter.continue_conversation = MagicMock(return_value=Future())
        mock_adapter.continue_conversation.return_value.set_result(Mock())
        mock_adapter.send_activities = MagicMock(return_value=Future())
        mock_adapter.send_activities.return_value.set_result([])

        sut = self.create_skill_handler_for_testing(mock_adapter)

        activity = Activity(type=ActivityTypes.message, attachments=[], entities=[])
        TurnContext.apply_conversation_reference(activity, self._conversation_reference)

        assert not activity.caller_id

        await sut.test_on_send_to_conversation(
            self._claims_identity, self._conversation_id, activity
        )

        args, kwargs = mock_adapter.continue_conversation.call_args_list[0]

        assert isinstance(args[0], ConversationReference)
        assert callable(args[1])
        assert isinstance(kwargs["claims_identity"], ClaimsIdentity)

        await args[1](
            TurnContext(
                mock_adapter,
                conversation_reference_extension.get_continuation_activity(
                    self._conversation_reference
                ),
            )
        )
        assert activity.caller_id is None

    async def test_forwarding_on_send_to_conversation(self):
        self._conversation_id = await self._test_id_factory.create_skill_conversation_id(
            self._conversation_reference
        )

        resource_response_id = "rId"

        async def side_effect(
            *arg_list, **args_dict
        ):  # pylint: disable=unused-argument
            fake_context = Mock()
            fake_context.turn_state = {}
            fake_context.send_activity = MagicMock(return_value=Future())
            fake_context.send_activity.return_value.set_result(
                ResourceResponse(id=resource_response_id)
            )
            await arg_list[1](fake_context)

        mock_adapter = Mock()
        mock_adapter.continue_conversation = side_effect
        mock_adapter.send_activities = MagicMock(return_value=Future())
        mock_adapter.send_activities.return_value.set_result([])

        sut = self.create_skill_handler_for_testing(mock_adapter)

        activity = Activity(type=ActivityTypes.message, attachments=[], entities=[])
        TurnContext.apply_conversation_reference(activity, self._conversation_reference)

        assert not activity.caller_id

        response = await sut.test_on_send_to_conversation(
            self._claims_identity, self._conversation_id, activity
        )

        assert response.id is resource_response_id

    async def test_on_reply_to_activity(self):
        self._conversation_id = await self._test_id_factory.create_skill_conversation_id(
            self._conversation_reference
        )

        mock_adapter = Mock()
        mock_adapter.continue_conversation = MagicMock(return_value=Future())
        mock_adapter.continue_conversation.return_value.set_result(Mock())
        mock_adapter.send_activities = MagicMock(return_value=Future())
        mock_adapter.send_activities.return_value.set_result([])

        sut = self.create_skill_handler_for_testing(mock_adapter)

        activity = Activity(type=ActivityTypes.message, attachments=[], entities=[])
        activity_id = str(uuid4())
        TurnContext.apply_conversation_reference(activity, self._conversation_reference)

        await sut.test_on_reply_to_activity(
            self._claims_identity, self._conversation_id, activity_id, activity
        )

        args, kwargs = mock_adapter.continue_conversation.call_args_list[0]

        assert isinstance(args[0], ConversationReference)
        assert callable(args[1])
        assert isinstance(kwargs["claims_identity"], ClaimsIdentity)

        await args[1](
            TurnContext(
                mock_adapter,
                conversation_reference_extension.get_continuation_activity(
                    self._conversation_reference
                ),
            )
        )
        assert activity.caller_id is None

    async def test_on_update_activity(self):
        self._conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)

        activity = Activity(type=ActivityTypes.message, attachments=[], entities=[])
        activity_id = str(uuid4())

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_update_activity(
                self._claims_identity, self._conversation_id, activity_id, activity
            )

    async def test_on_delete_activity(self):
        self._conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)
        activity_id = str(uuid4())

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_delete_activity(
                self._claims_identity, self._conversation_id, activity_id
            )

    async def test_on_get_activity_members(self):
        self._conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)
        activity_id = str(uuid4())

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_get_activity_members(
                self._claims_identity, self._conversation_id, activity_id
            )

    async def test_on_create_conversation(self):
        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)
        conversation_parameters = ConversationParameters()

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_create_conversation(
                self._claims_identity, conversation_parameters
            )

    async def test_on_get_conversations(self):
        self._conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_get_conversations(
                self._claims_identity, self._conversation_id
            )

    async def test_on_get_conversation_members(self):
        self._conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_get_conversation_members(
                self._claims_identity, self._conversation_id
            )

    async def test_on_get_conversation_paged_members(self):
        self._conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_get_conversation_paged_members(
                self._claims_identity, self._conversation_id
            )

    async def test_on_delete_conversation_member(self):
        self._conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)
        member_id = str(uuid4())

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_delete_conversation_member(
                self._claims_identity, self._conversation_id, member_id
            )

    async def test_on_send_conversation_history(self):
        self._conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)
        transcript = Transcript()

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_send_conversation_history(
                self._claims_identity, self._conversation_id, transcript
            )

    async def test_on_upload_attachment(self):
        self._conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)
        attachment_data = AttachmentData()

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_upload_attachment(
                self._claims_identity, self._conversation_id, attachment_data
            )

    async def test_event_activity(self):
        activity = Activity(type=ActivityTypes.event)
        await self.__activity_callback_test(activity)
        assert (
            activity.caller_id
            == f"{CallerIdConstants.bot_to_bot_prefix}{self.skill_id}"
        )

    async def test_eoc_activity(self):
        activity = Activity(type=ActivityTypes.end_of_conversation)
        await self.__activity_callback_test(activity)
        assert (
            activity.caller_id
            == f"{CallerIdConstants.bot_to_bot_prefix}{self.skill_id}"
        )

    async def __activity_callback_test(self, activity: Activity):
        self._conversation_id = await self._test_id_factory.create_skill_conversation_id(
            self._conversation_reference
        )

        mock_adapter = Mock()
        mock_adapter.continue_conversation = MagicMock(return_value=Future())
        mock_adapter.continue_conversation.return_value.set_result(Mock())
        mock_adapter.send_activities = MagicMock(return_value=Future())
        mock_adapter.send_activities.return_value.set_result([])

        sut = self.create_skill_handler_for_testing(mock_adapter)

        activity_id = str(uuid4())
        TurnContext.apply_conversation_reference(activity, self._conversation_reference)

        await sut.test_on_reply_to_activity(
            self._claims_identity, self._conversation_id, activity_id, activity
        )

        args, kwargs = mock_adapter.continue_conversation.call_args_list[0]

        assert isinstance(args[0], ConversationReference)
        assert callable(args[1])
        assert isinstance(kwargs["claims_identity"], ClaimsIdentity)

        await args[1](TurnContext(mock_adapter, activity))
