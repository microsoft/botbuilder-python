# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import uuid4
from typing import Awaitable, Callable, Dict, Union


from unittest.mock import Mock
import aiounittest

from botbuilder.core import MessageFactory, InvokeResponse
from botbuilder.core.skills import (
    BotFrameworkSkill,
    ConversationIdFactoryBase,
    SkillConversationIdFactoryOptions,
    SkillConversationReference,
)
from botbuilder.integration.aiohttp.skills import SkillHttpClient
from botbuilder.schema import Activity, ConversationAccount, ConversationReference
from botframework.connector.auth import (
    AuthenticationConstants,
    ChannelProvider,
    GovernmentConstants,
)


class SimpleConversationIdFactory(ConversationIdFactoryBase):
    def __init__(self, conversation_id: str):
        self._conversation_id = conversation_id
        self._conversation_refs: Dict[str, SkillConversationReference] = {}
        # Public property to capture and assert the options passed to CreateSkillConversationIdAsync.
        self.creation_options: SkillConversationIdFactoryOptions = None

    async def create_skill_conversation_id(
        self,
        options_or_conversation_reference: Union[
            SkillConversationIdFactoryOptions, ConversationReference
        ],
    ) -> str:
        self.creation_options = options_or_conversation_reference

        key = self._conversation_id
        self._conversation_refs[key] = self._conversation_refs.get(
            key,
            SkillConversationReference(
                conversation_reference=options_or_conversation_reference.activity.get_conversation_reference(),
                oauth_scope=options_or_conversation_reference.from_bot_oauth_scope,
            ),
        )
        return key

    async def get_skill_conversation_reference(
        self, skill_conversation_id: str
    ) -> SkillConversationReference:
        return self._conversation_refs[skill_conversation_id]

    async def delete_conversation_reference(self, skill_conversation_id: str):
        raise NotImplementedError()


class TestSkillHttpClientTests(aiounittest.AsyncTestCase):
    async def test_post_activity_with_originating_audience(self):
        conversation_id = str(uuid4())
        conversation_id_factory = SimpleConversationIdFactory(conversation_id)
        test_activity = MessageFactory.text("some message")
        test_activity.conversation = ConversationAccount()
        skill = BotFrameworkSkill(
            id="SomeSkill",
            app_id="",
            skill_endpoint="https://someskill.com/api/messages",
        )

        async def _mock_post_content(
            to_url: str,
            token: str,  # pylint: disable=unused-argument
            activity: Activity,
        ) -> (int, object):
            nonlocal self
            self.assertEqual(skill.skill_endpoint, to_url)
            # Assert that the activity being sent has what we expect.
            self.assertEqual(conversation_id, activity.conversation.id)
            self.assertEqual("https://parentbot.com/api/messages", activity.service_url)

            # Create mock response.
            return 200, None

        sut = await self._create_http_client_with_mock_handler(
            _mock_post_content, conversation_id_factory
        )

        result = await sut.post_activity_to_skill(
            "",
            skill,
            "https://parentbot.com/api/messages",
            test_activity,
            "someOriginatingAudience",
        )

        # Assert factory options
        self.assertEqual("", conversation_id_factory.creation_options.from_bot_id)
        self.assertEqual(
            "someOriginatingAudience",
            conversation_id_factory.creation_options.from_bot_oauth_scope,
        )
        self.assertEqual(
            test_activity, conversation_id_factory.creation_options.activity
        )
        self.assertEqual(
            skill, conversation_id_factory.creation_options.bot_framework_skill
        )

        # Assert result
        self.assertIsInstance(result, InvokeResponse)
        self.assertEqual(200, result.status)

    async def test_post_activity_using_invoke_response(self):
        for is_gov in [True, False]:
            with self.subTest(is_government=is_gov):
                # pylint: disable=undefined-variable
                # pylint: disable=cell-var-from-loop
                conversation_id = str(uuid4())
                conversation_id_factory = SimpleConversationIdFactory(conversation_id)
                test_activity = MessageFactory.text("some message")
                test_activity.conversation = ConversationAccount()
                expected_oauth_scope = (
                    AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
                )
                mock_channel_provider: ChannelProvider = Mock(spec=ChannelProvider)

                def is_government_mock():
                    nonlocal expected_oauth_scope
                    if is_government:
                        expected_oauth_scope = (
                            GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
                        )

                    return is_government

                mock_channel_provider.is_government = Mock(
                    side_effect=is_government_mock
                )

                skill = BotFrameworkSkill(
                    id="SomeSkill",
                    app_id="",
                    skill_endpoint="https://someskill.com/api/messages",
                )

                async def _mock_post_content(
                    to_url: str,
                    token: str,  # pylint: disable=unused-argument
                    activity: Activity,
                ) -> (int, object):
                    nonlocal self

                    self.assertEqual(skill.skill_endpoint, to_url)
                    # Assert that the activity being sent has what we expect.
                    self.assertEqual(conversation_id, activity.conversation.id)
                    self.assertEqual(
                        "https://parentbot.com/api/messages", activity.service_url
                    )

                    # Create mock response.
                    return 200, None

                sut = await self._create_http_client_with_mock_handler(
                    _mock_post_content, conversation_id_factory
                )
                result = await sut.post_activity_to_skill(
                    "", skill, "https://parentbot.com/api/messages", test_activity
                )

                # Assert factory options
                self.assertEqual(
                    "", conversation_id_factory.creation_options.from_bot_id
                )
                self.assertEqual(
                    expected_oauth_scope,
                    conversation_id_factory.creation_options.from_bot_oauth_scope,
                )
                self.assertEqual(
                    test_activity, conversation_id_factory.creation_options.activity
                )
                self.assertEqual(
                    skill, conversation_id_factory.creation_options.bot_framework_skill
                )

                # Assert result
                self.assertIsInstance(result, InvokeResponse)
                self.assertEqual(200, result.status)

    # Helper to create an HttpClient with a mock message handler that executes function argument to validate the request
    # and mock a response.
    async def _create_http_client_with_mock_handler(
        self,
        value_function: Callable[[object], Awaitable[object]],
        id_factory: ConversationIdFactoryBase,
        channel_provider: ChannelProvider = None,
    ) -> SkillHttpClient:
        # pylint: disable=protected-access
        client = SkillHttpClient(Mock(), id_factory, channel_provider)
        client._post_content = value_function
        await client._session.close()

        return client
