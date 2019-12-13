import aiounittest

from botbuilder.core.teams.teams_helper import deserializer_helper
from botbuilder.schema import Activity, ChannelAccount, Mention
from botbuilder.schema.teams import (
    MessageActionsPayload,
    MessagingExtensionAction,
    TaskModuleRequestContext,
)


class TestTeamsActivityHandler(aiounittest.AsyncTestCase):
    def test_teams_helper_teams_schema(self):
        # Arrange
        data = {
            "data": {"key": "value"},
            "context": {"theme": "dark"},
            "commandId": "test_command",
            "commandContext": "command_context_test",
            "botMessagePreviewAction": "edit",
            "botActivityPreview": [{"id": "activity123"}],
            "messagePayload": {"id": "payloadid"},
        }

        # Act
        result = deserializer_helper(MessagingExtensionAction, data)

        # Assert
        assert result.data == {"key": "value"}
        assert result.context == TaskModuleRequestContext(theme="dark")
        assert result.command_id == "test_command"
        assert result.bot_message_preview_action == "edit"
        assert len(result.bot_activity_preview) == 1
        assert result.bot_activity_preview[0] == Activity(id="activity123")
        assert result.message_payload == MessageActionsPayload(id="payloadid")

    def test_teams_helper_schema(self):
        # Arrange
        data = {
            "mentioned": {"id": "123", "name": "testName"},
            "text": "Hello <at>testName</at>",
            "type": "mention",
        }

        # Act
        result = deserializer_helper(Mention, data)

        # Assert
        assert result.mentioned == ChannelAccount(id="123", name="testName")
        assert result.text == "Hello <at>testName</at>"
        assert result.type == "mention"
