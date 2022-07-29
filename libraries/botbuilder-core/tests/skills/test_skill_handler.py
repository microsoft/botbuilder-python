# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import hashlib
import json
from datetime import datetime
from uuid import uuid4
from asyncio import Future
from typing import Dict, List, Callable

from unittest.mock import Mock, MagicMock
import aiounittest

from botframework.connector.auth import (
    AuthenticationConfiguration,
    AuthenticationConstants,
    ClaimsIdentity,
)
from botbuilder.core import (
    TurnContext,
    BotActionNotImplementedError,
    conversation_reference_extension,
)
from botbuilder.core.skills import (
    ConversationIdFactoryBase,
    SkillHandler,
    SkillConversationReference,
    SkillConversationIdFactoryOptions,
    BotFrameworkSkill,
)
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


class ConversationIdFactoryForTest(
    ConversationIdFactoryBase
):  # pylint: disable=abstract-method
    def __init__(self):
        self._conversation_refs: Dict[str, str] = {}

    async def create_skill_conversation_id(  # pylint: disable=W0221
        self, options: SkillConversationIdFactoryOptions
    ) -> str:
        conversation_reference = TurnContext.get_conversation_reference(
            options.activity
        )

        key = hashlib.md5(
            f"{conversation_reference.conversation.id}{conversation_reference.service_url}".encode()
        ).hexdigest()

        skill_conversation_reference = SkillConversationReference(
            conversation_reference=conversation_reference,
            oauth_scope=options.from_bot_oauth_scope,
        )

        self._conversation_refs[key] = skill_conversation_reference

        return key

    async def get_skill_conversation_reference(
        self, skill_conversation_id: str
    ) -> SkillConversationReference:
        return self._conversation_refs[skill_conversation_id]

    async def delete_conversation_reference(self, skill_conversation_id: str):
        pass


class LegacyConversationIdFactoryForTest(
    ConversationIdFactoryBase
):  # pylint: disable=abstract-method
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
        self,
        claims_identity: ClaimsIdentity,
        continuation_token: str = "",
    ) -> ConversationsResult:
        return await self.on_get_conversations(claims_identity, continuation_token)

    async def test_on_create_conversation(
        self,
        claims_identity: ClaimsIdentity,
        parameters: ConversationParameters,
    ) -> ConversationResourceResponse:
        return await self.on_create_conversation(claims_identity, parameters)

    async def test_on_send_to_conversation(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity: Activity,
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
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity_id: str,
    ):
        return await self.on_delete_activity(
            claims_identity, conversation_id, activity_id
        )

    async def test_on_get_conversation_members(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
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
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        member_id: str,
    ):
        return await self.on_delete_conversation_member(
            claims_identity, conversation_id, member_id
        )

    async def test_on_get_activity_members(
        self,
        claims_identity: ClaimsIdentity,
        conversation_id: str,
        activity_id: str,
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
        activity = Activity.create_message_activity()
        activity.apply_conversation_reference(cls._conversation_reference)
        skill = BotFrameworkSkill(
            app_id=cls.skill_id,
            id="skill",
            skill_endpoint="http://testbot.com/api/messages",
        )
        cls._options = SkillConversationIdFactoryOptions(
            from_bot_oauth_scope=cls.bot_id,
            from_bot_id=cls.bot_id,
            activity=activity,
            bot_framework_skill=skill,
        )

    def create_skill_handler_for_testing(
        self, adapter, factory: ConversationIdFactoryBase = None
    ) -> SkillHandlerInstanceForTests:
        mock_bot = Mock()
        mock_bot.on_turn = MagicMock(return_value=Future())
        mock_bot.on_turn.return_value.set_result(Mock())

        return SkillHandlerInstanceForTests(
            adapter,
            mock_bot,
            (factory or self._test_id_factory),
            Mock(),
            AuthenticationConfiguration(),
        )

    async def test_legacy_conversation_id_factory(self):
        mock_adapter = Mock()

        legacy_factory = LegacyConversationIdFactoryForTest()
        conversation_reference = ConversationReference(
            conversation=ConversationAccount(id=str(uuid4())),
            service_url="http://testbot.com/api/messages",
        )

        conversation_id = await legacy_factory.create_skill_conversation_id(
            conversation_reference
        )

        async def continue_conversation(
            reference: ConversationReference,
            callback: Callable,
            bot_id: str = None,
            claims_identity: ClaimsIdentity = None,
            audience: str = None,
        ):  # pylint: disable=unused-argument
            # Invoke the callback created by the handler so we can assert the rest of the execution.
            turn_context = TurnContext(
                mock_adapter,
                conversation_reference_extension.get_continuation_activity(
                    conversation_reference
                ),
            )
            await callback(turn_context)

        async def send_activities(
            context: TurnContext, activities: List[Activity]
        ):  # pylint: disable=unused-argument
            return [ResourceResponse(id="resourceId")]

        mock_adapter.continue_conversation = continue_conversation
        mock_adapter.send_activities = send_activities

        activity = Activity.create_message_activity()
        activity.apply_conversation_reference(conversation_reference)

        sut = self.create_skill_handler_for_testing(mock_adapter, legacy_factory)
        await sut.test_on_send_to_conversation(
            self._claims_identity, conversation_id, activity
        )

    async def test_on_send_to_conversation(self):
        conversation_id = await self._test_id_factory.create_skill_conversation_id(
            self._options
        )

        # python 3.7 doesn't support AsyncMock, change this when min ver is 3.8
        send_activities_called = False

        mock_adapter = Mock()

        async def continue_conversation(
            reference: ConversationReference,
            callback: Callable,
            bot_id: str = None,
            claims_identity: ClaimsIdentity = None,
            audience: str = None,
        ):  # pylint: disable=unused-argument
            # Invoke the callback created by the handler so we can assert the rest of the execution.
            turn_context = TurnContext(
                mock_adapter,
                conversation_reference_extension.get_continuation_activity(
                    self._conversation_reference
                ),
            )
            await callback(turn_context)

            # Assert the callback set the right properties.
            assert (
                f"{CallerIdConstants.bot_to_bot_prefix}{self.skill_id}"
            ), turn_context.activity.caller_id

        async def send_activities(
            context: TurnContext, activities: List[Activity]
        ):  # pylint: disable=unused-argument
            # Messages should not have a caller id set when sent back to the caller.
            nonlocal send_activities_called
            assert activities[0].caller_id is None
            assert activities[0].reply_to_id is None
            send_activities_called = True
            return [ResourceResponse(id="resourceId")]

        mock_adapter.continue_conversation = continue_conversation
        mock_adapter.send_activities = send_activities

        types_to_test = [
            ActivityTypes.end_of_conversation,
            ActivityTypes.event,
            ActivityTypes.message,
        ]

        for activity_type in types_to_test:
            with self.subTest(act_type=activity_type):
                send_activities_called = False
                activity = Activity(type=activity_type, attachments=[], entities=[])
                TurnContext.apply_conversation_reference(
                    activity, self._conversation_reference
                )
                sut = self.create_skill_handler_for_testing(mock_adapter)

                resource_response = await sut.test_on_send_to_conversation(
                    self._claims_identity, conversation_id, activity
                )

                if activity_type == ActivityTypes.message:
                    assert send_activities_called
                    assert resource_response.id == "resourceId"

    async def test_forwarding_on_send_to_conversation(self):
        conversation_id = await self._test_id_factory.create_skill_conversation_id(
            self._options
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
            self._claims_identity, conversation_id, activity
        )

        assert response.id is resource_response_id

    async def test_on_reply_to_activity(self):
        resource_response_id = "resourceId"
        conversation_id = await self._test_id_factory.create_skill_conversation_id(
            self._options
        )

        types_to_test = [
            ActivityTypes.end_of_conversation,
            ActivityTypes.event,
            ActivityTypes.message,
        ]

        for activity_type in types_to_test:
            with self.subTest(act_type=activity_type):
                mock_adapter = Mock()
                mock_adapter.continue_conversation = MagicMock(return_value=Future())
                mock_adapter.continue_conversation.return_value.set_result(Mock())
                mock_adapter.send_activities = MagicMock(return_value=Future())
                mock_adapter.send_activities.return_value.set_result(
                    [ResourceResponse(id=resource_response_id)]
                )

                sut = self.create_skill_handler_for_testing(mock_adapter)

                activity = Activity(type=activity_type, attachments=[], entities=[])
                activity_id = str(uuid4())
                TurnContext.apply_conversation_reference(
                    activity, self._conversation_reference
                )

                resource_response = await sut.test_on_reply_to_activity(
                    self._claims_identity, conversation_id, activity_id, activity
                )

                # continue_conversation validation
                (
                    args_continue,
                    kwargs_continue,
                ) = mock_adapter.continue_conversation.call_args_list[0]
                mock_adapter.continue_conversation.assert_called_once()

                assert isinstance(args_continue[0], ConversationReference)
                assert callable(args_continue[1])
                assert isinstance(kwargs_continue["claims_identity"], ClaimsIdentity)

                turn_context = TurnContext(
                    mock_adapter,
                    conversation_reference_extension.get_continuation_activity(
                        self._conversation_reference
                    ),
                )
                await args_continue[1](turn_context)
                # assert the callback set the right properties.
                assert (
                    f"{CallerIdConstants.bot_to_bot_prefix}{self.skill_id}"
                ), turn_context.activity.caller_id

                if activity_type == ActivityTypes.message:
                    # send_activities validation
                    (
                        args_send,
                        _,
                    ) = mock_adapter.send_activities.call_args_list[0]
                    activity_from_send = args_send[1][0]
                    assert activity_from_send.caller_id is None
                    assert activity_from_send.reply_to_id, activity_id
                    assert resource_response.id, resource_response_id
                else:
                    # Assert mock SendActivitiesAsync wasn't called
                    mock_adapter.send_activities.assert_not_called()

    async def test_on_update_activity(self):
        conversation_id = await self._test_id_factory.create_skill_conversation_id(
            self._options
        )
        resource_response_id = "resourceId"
        called_continue = False
        called_update = False

        mock_adapter = Mock()
        activity = Activity(type=ActivityTypes.message, attachments=[], entities=[])
        activity_id = str(uuid4())
        message = activity.text = f"TestUpdate {datetime.now()}."

        async def continue_conversation(
            reference: ConversationReference,
            callback: Callable,
            bot_id: str = None,
            claims_identity: ClaimsIdentity = None,
            audience: str = None,
        ):  # pylint: disable=unused-argument
            # Invoke the callback created by the handler so we can assert the rest of the execution.
            nonlocal called_continue
            turn_context = TurnContext(
                mock_adapter,
                conversation_reference_extension.get_continuation_activity(
                    self._conversation_reference
                ),
            )
            await callback(turn_context)

            # Assert the callback set the right properties.
            assert (
                f"{CallerIdConstants.bot_to_bot_prefix}{self.skill_id}"
            ), turn_context.activity.caller_id
            called_continue = True

        async def update_activity(
            context: TurnContext,  # pylint: disable=unused-argument
            new_activity: Activity,
        ) -> ResourceResponse:
            # Assert the activity being sent.
            nonlocal called_update
            assert activity_id, new_activity.reply_to_id
            assert message, new_activity.text
            called_update = True

            return ResourceResponse(id=resource_response_id)

        mock_adapter.continue_conversation = continue_conversation
        mock_adapter.update_activity = update_activity

        sut = self.create_skill_handler_for_testing(mock_adapter)
        resource_response = await sut.test_on_update_activity(
            self._claims_identity, conversation_id, activity_id, activity
        )

        assert called_continue
        assert called_update
        assert resource_response, resource_response_id

    async def test_on_delete_activity(self):
        conversation_id = await self._test_id_factory.create_skill_conversation_id(
            self._options
        )

        resource_response_id = "resourceId"
        called_continue = False
        called_delete = False

        mock_adapter = Mock()
        activity_id = str(uuid4())

        async def continue_conversation(
            reference: ConversationReference,
            callback: Callable,
            bot_id: str = None,
            claims_identity: ClaimsIdentity = None,
            audience: str = None,
        ):  # pylint: disable=unused-argument
            # Invoke the callback created by the handler so we can assert the rest of the execution.
            nonlocal called_continue
            turn_context = TurnContext(
                mock_adapter,
                conversation_reference_extension.get_continuation_activity(
                    self._conversation_reference
                ),
            )
            await callback(turn_context)
            called_continue = True

        async def delete_activity(
            context: TurnContext,  # pylint: disable=unused-argument
            conversation_reference: ConversationReference,
        ) -> ResourceResponse:
            # Assert the activity being sent.
            nonlocal called_delete
            # Assert the activity_id being deleted.
            assert activity_id, conversation_reference.activity_id
            called_delete = True

            return ResourceResponse(id=resource_response_id)

        mock_adapter.continue_conversation = continue_conversation
        mock_adapter.delete_activity = delete_activity

        sut = self.create_skill_handler_for_testing(mock_adapter)

        await sut.test_on_delete_activity(
            self._claims_identity, conversation_id, activity_id
        )

        assert called_continue
        assert called_delete

    async def test_on_get_activity_members(self):
        conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)
        activity_id = str(uuid4())

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_get_activity_members(
                self._claims_identity, conversation_id, activity_id
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
        conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_get_conversations(self._claims_identity, conversation_id)

    async def test_on_get_conversation_members(self):
        conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_get_conversation_members(
                self._claims_identity, conversation_id
            )

    async def test_on_get_conversation_paged_members(self):
        conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_get_conversation_paged_members(
                self._claims_identity, conversation_id
            )

    async def test_on_delete_conversation_member(self):
        conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)
        member_id = str(uuid4())

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_delete_conversation_member(
                self._claims_identity, conversation_id, member_id
            )

    async def test_on_send_conversation_history(self):
        conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)
        transcript = Transcript()

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_send_conversation_history(
                self._claims_identity, conversation_id, transcript
            )

    async def test_on_upload_attachment(self):
        conversation_id = ""

        mock_adapter = Mock()

        sut = self.create_skill_handler_for_testing(mock_adapter)
        attachment_data = AttachmentData()

        with self.assertRaises(BotActionNotImplementedError):
            await sut.test_on_upload_attachment(
                self._claims_identity, conversation_id, attachment_data
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
        conversation_id = await self._test_id_factory.create_skill_conversation_id(
            self._options
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
            self._claims_identity, conversation_id, activity_id, activity
        )

        args, kwargs = mock_adapter.continue_conversation.call_args_list[0]

        assert isinstance(args[0], ConversationReference)
        assert callable(args[1])
        assert isinstance(kwargs["claims_identity"], ClaimsIdentity)

        await args[1](TurnContext(mock_adapter, activity))
