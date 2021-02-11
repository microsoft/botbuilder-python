from unittest.mock import Mock

import aiounittest
from botbuilder.schema import ConversationAccount, ChannelAccount, RoleTypes
from botbuilder.integration.aiohttp import BotFrameworkHttpClient
from botframework.connector.auth import CredentialProvider, Activity


class TestBotFrameworkHttpClient(aiounittest.AsyncTestCase):
    async def test_should_create_connector_client(self):
        with self.assertRaises(TypeError):
            BotFrameworkHttpClient(None)

    async def test_adds_recipient_and_sets_it_back_to_null(self):
        mock_credential_provider = Mock(spec=CredentialProvider)

        # pylint: disable=unused-argument
        async def _mock_post_content(
            to_url: str, token: str, activity: Activity
        ) -> (int, object):
            nonlocal self
            self.assertIsNotNone(activity.recipient)
            return 200, None

        client = BotFrameworkHttpClient(credential_provider=mock_credential_provider)
        client._post_content = _mock_post_content  # pylint: disable=protected-access

        activity = Activity(conversation=ConversationAccount())

        await client.post_activity(
            None,
            None,
            "https://skillbot.com/api/messages",
            "https://parentbot.com/api/messages",
            "NewConversationId",
            activity,
        )

        assert activity.recipient is None

    async def test_does_not_overwrite_non_null_recipient_values(self):
        skill_recipient_id = "skillBot"
        mock_credential_provider = Mock(spec=CredentialProvider)

        # pylint: disable=unused-argument
        async def _mock_post_content(
            to_url: str, token: str, activity: Activity
        ) -> (int, object):
            nonlocal self
            self.assertIsNotNone(activity.recipient)
            self.assertEqual(skill_recipient_id, activity.recipient.id)
            return 200, None

        client = BotFrameworkHttpClient(credential_provider=mock_credential_provider)
        client._post_content = _mock_post_content  # pylint: disable=protected-access

        activity = Activity(
            conversation=ConversationAccount(),
            recipient=ChannelAccount(id=skill_recipient_id),
        )

        await client.post_activity(
            None,
            None,
            "https://skillbot.com/api/messages",
            "https://parentbot.com/api/messages",
            "NewConversationId",
            activity,
        )

        assert activity.recipient.id == skill_recipient_id
        assert activity.recipient.role is RoleTypes.skill
