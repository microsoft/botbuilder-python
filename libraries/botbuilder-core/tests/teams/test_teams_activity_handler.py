from typing import List

import aiounittest
from botbuilder.core import BotAdapter, TurnContext
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    ConversationAccount,
    ConversationReference,
    ResourceResponse,
)
from botbuilder.schema.teams import (
    AppBasedLinkQuery,
    ChannelInfo,
    FileConsentCardResponse,
    MessageActionsPayload,
    MessagingExtensionAction,
    MessagingExtensionQuery,
    O365ConnectorCardActionQuery,
    TaskModuleRequest,
    TaskModuleRequestContext,
    TeamInfo,
    TeamsChannelAccount,
)
from botframework.connector import Channels
from simple_adapter import SimpleAdapter


class TestingTeamsActivityHandler(TeamsActivityHandler):
    __test__ = False

    def __init__(self):
        self.record: List[str] = []

    async def on_conversation_update_activity(self, turn_context: TurnContext):
        self.record.append("on_conversation_update_activity")
        return await super().on_conversation_update_activity(turn_context)

    async def on_teams_members_added(  # pylint: disable=unused-argument
        self,
        teams_members_added: [TeamsChannelAccount],
        team_info: TeamInfo,
        turn_context: TurnContext,
    ):
        self.record.append("on_teams_members_added")
        return await super().on_teams_members_added(
            teams_members_added, team_info, turn_context
        )

    async def on_teams_members_removed(
        self,
        teams_members_removed: [TeamsChannelAccount],
        team_info: TeamInfo,
        turn_context: TurnContext,
    ):
        self.record.append("on_teams_members_removed")
        return await super().on_teams_members_removed(
            teams_members_removed, team_info, turn_context
        )

    async def on_message_activity(self, turn_context: TurnContext):
        self.record.append("on_message_activity")
        return await super().on_message_activity(turn_context)

    async def on_token_response_event(self, turn_context: TurnContext):
        self.record.append("on_token_response_event")
        return await super().on_token_response_event(turn_context)

    async def on_event(self, turn_context: TurnContext):
        self.record.append("on_event")
        return await super().on_event(turn_context)

    async def on_end_of_conversation_activity(self, turn_context: TurnContext):
        self.record.append("on_end_of_conversation_activity")
        return await super().on_end_of_conversation_activity(turn_context)

    async def on_typing_activity(self, turn_context: TurnContext):
        self.record.append("on_typing_activity")
        return await super().on_typing_activity(turn_context)

    async def on_unrecognized_activity_type(self, turn_context: TurnContext):
        self.record.append("on_unrecognized_activity_type")
        return await super().on_unrecognized_activity_type(turn_context)

    async def on_teams_channel_created(
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        self.record.append("on_teams_channel_created")
        return await super().on_teams_channel_created(
            channel_info, team_info, turn_context
        )

    async def on_teams_channel_renamed(
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        self.record.append("on_teams_channel_renamed")
        return await super().on_teams_channel_renamed(
            channel_info, team_info, turn_context
        )

    async def on_teams_channel_deleted(
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        self.record.append("on_teams_channel_deleted")
        return await super().on_teams_channel_renamed(
            channel_info, team_info, turn_context
        )

    async def on_teams_team_renamed_activity(
        self, team_info: TeamInfo, turn_context: TurnContext
    ):
        self.record.append("on_teams_team_renamed_activity")
        return await super().on_teams_team_renamed_activity(team_info, turn_context)

    async def on_invoke_activity(self, turn_context: TurnContext):
        self.record.append("on_invoke_activity")
        return await super().on_invoke_activity(turn_context)

    async def on_teams_signin_verify_state(self, turn_context: TurnContext):
        self.record.append("on_teams_signin_verify_state")
        return await super().on_teams_signin_verify_state(turn_context)

    async def on_teams_file_consent(
        self,
        turn_context: TurnContext,
        file_consent_card_response: FileConsentCardResponse,
    ):
        self.record.append("on_teams_file_consent")
        return await super().on_teams_file_consent(
            turn_context, file_consent_card_response
        )

    async def on_teams_file_consent_accept(
        self,
        turn_context: TurnContext,
        file_consent_card_response: FileConsentCardResponse,
    ):
        self.record.append("on_teams_file_consent_accept")
        return await super().on_teams_file_consent_accept(
            turn_context, file_consent_card_response
        )

    async def on_teams_file_consent_decline(
        self,
        turn_context: TurnContext,
        file_consent_card_response: FileConsentCardResponse,
    ):
        self.record.append("on_teams_file_consent_decline")
        return await super().on_teams_file_consent_decline(
            turn_context, file_consent_card_response
        )

    async def on_teams_o365_connector_card_action(
        self, turn_context: TurnContext, query: O365ConnectorCardActionQuery
    ):
        self.record.append("on_teams_o365_connector_card_action")
        return await super().on_teams_o365_connector_card_action(turn_context, query)

    async def on_teams_app_based_link_query(
        self, turn_context: TurnContext, query: AppBasedLinkQuery
    ):
        self.record.append("on_teams_app_based_link_query")
        return await super().on_teams_app_based_link_query(turn_context, query)

    async def on_teams_messaging_extension_query(
        self, turn_context: TurnContext, query: MessagingExtensionQuery
    ):
        self.record.append("on_teams_messaging_extension_query")
        return await super().on_teams_messaging_extension_query(turn_context, query)

    async def on_teams_messaging_extension_submit_action_dispatch(
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ):
        self.record.append("on_teams_messaging_extension_submit_action_dispatch")
        return await super().on_teams_messaging_extension_submit_action_dispatch(
            turn_context, action
        )

    async def on_teams_messaging_extension_submit_action(
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ):
        self.record.append("on_teams_messaging_extension_submit_action")
        return await super().on_teams_messaging_extension_submit_action(
            turn_context, action
        )

    async def on_teams_messaging_extension_bot_message_preview_edit(
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ):
        self.record.append("on_teams_messaging_extension_bot_message_preview_edit")
        return await super().on_teams_messaging_extension_bot_message_preview_edit(
            turn_context, action
        )

    async def on_teams_messaging_extension_bot_message_preview_send(
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ):
        self.record.append("on_teams_messaging_extension_bot_message_preview_send")
        return await super().on_teams_messaging_extension_bot_message_preview_send(
            turn_context, action
        )

    async def on_teams_messaging_extension_fetch_task(
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ):
        self.record.append("on_teams_messaging_extension_fetch_task")
        return await super().on_teams_messaging_extension_fetch_task(
            turn_context, action
        )

    async def on_teams_messaging_extension_configuration_query_settings_url(
        self, turn_context: TurnContext, query: MessagingExtensionQuery
    ):
        self.record.append(
            "on_teams_messaging_extension_configuration_query_settings_url"
        )
        return await super().on_teams_messaging_extension_configuration_query_settings_url(
            turn_context, query
        )

    async def on_teams_messaging_extension_configuration_setting(
        self, turn_context: TurnContext, settings
    ):
        self.record.append("on_teams_messaging_extension_configuration_setting")
        return await super().on_teams_messaging_extension_configuration_setting(
            turn_context, settings
        )

    async def on_teams_messaging_extension_card_button_clicked(
        self, turn_context: TurnContext, card_data
    ):
        self.record.append("on_teams_messaging_extension_card_button_clicked")
        return await super().on_teams_messaging_extension_card_button_clicked(
            turn_context, card_data
        )

    async def on_teams_task_module_fetch(
        self, turn_context: TurnContext, task_module_request
    ):
        self.record.append("on_teams_task_module_fetch")
        return await super().on_teams_task_module_fetch(
            turn_context, task_module_request
        )

    async def on_teams_task_module_submit(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, task_module_request: TaskModuleRequest
    ):
        self.record.append("on_teams_task_module_submit")
        return await super().on_teams_task_module_submit(
            turn_context, task_module_request
        )


class NotImplementedAdapter(BotAdapter):
    async def delete_activity(
        self, context: TurnContext, reference: ConversationReference
    ):
        raise NotImplementedError()

    async def send_activities(
        self, context: TurnContext, activities: List[Activity]
    ) -> List[ResourceResponse]:
        raise NotImplementedError()

    async def update_activity(self, context: TurnContext, activity: Activity):
        raise NotImplementedError()


class TestTeamsActivityHandler(aiounittest.AsyncTestCase):
    async def test_on_teams_channel_created_activity(self):
        # arrange
        activity = Activity(
            type=ActivityTypes.conversation_update,
            channel_data={
                "eventType": "channelCreated",
                "channel": {"id": "asdfqwerty", "name": "new_channel"},
            },
            channel_id=Channels.ms_teams,
        )

        turn_context = TurnContext(NotImplementedAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_conversation_update_activity"
        assert bot.record[1] == "on_teams_channel_created"

    async def test_on_teams_channel_renamed_activity(self):
        # arrange
        activity = Activity(
            type=ActivityTypes.conversation_update,
            channel_data={
                "eventType": "channelRenamed",
                "channel": {"id": "asdfqwerty", "name": "new_channel"},
            },
            channel_id=Channels.ms_teams,
        )

        turn_context = TurnContext(NotImplementedAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_conversation_update_activity"
        assert bot.record[1] == "on_teams_channel_renamed"

    async def test_on_teams_channel_deleted_activity(self):
        # arrange
        activity = Activity(
            type=ActivityTypes.conversation_update,
            channel_data={
                "eventType": "channelDeleted",
                "channel": {"id": "asdfqwerty", "name": "new_channel"},
            },
            channel_id=Channels.ms_teams,
        )

        turn_context = TurnContext(NotImplementedAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_conversation_update_activity"
        assert bot.record[1] == "on_teams_channel_deleted"

    async def test_on_teams_team_renamed_activity(self):
        # arrange
        activity = Activity(
            type=ActivityTypes.conversation_update,
            channel_data={
                "eventType": "teamRenamed",
                "team": {"id": "team_id_1", "name": "new_team_name"},
            },
            channel_id=Channels.ms_teams,
        )

        turn_context = TurnContext(NotImplementedAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_conversation_update_activity"
        assert bot.record[1] == "on_teams_team_renamed_activity"

    async def test_on_teams_members_added_activity(self):
        # arrange
        activity = Activity(
            type=ActivityTypes.conversation_update,
            channel_data={
                "eventType": "teamMemberAdded",
                "team": {"id": "team_id_1", "name": "new_team_name"},
            },
            members_added=[
                ChannelAccount(
                    id="123",
                    name="test_user",
                    aad_object_id="asdfqwerty",
                    role="tester",
                )
            ],
            channel_id=Channels.ms_teams,
            conversation=ConversationAccount(id="456"),
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_conversation_update_activity"
        assert bot.record[1] == "on_teams_members_added"

    async def test_bot_on_teams_members_added_activity(self):
        # arrange
        activity = Activity(
            recipient=ChannelAccount(id="botid"),
            type=ActivityTypes.conversation_update,
            channel_data={
                "eventType": "teamMemberAdded",
                "team": {"id": "team_id_1", "name": "new_team_name"},
            },
            members_added=[
                ChannelAccount(
                    id="botid",
                    name="test_user",
                    aad_object_id="asdfqwerty",
                    role="tester",
                )
            ],
            channel_id=Channels.ms_teams,
            conversation=ConversationAccount(id="456"),
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_conversation_update_activity"
        assert bot.record[1] == "on_teams_members_added"

    async def test_on_teams_members_removed_activity(self):
        # arrange
        activity = Activity(
            type=ActivityTypes.conversation_update,
            channel_data={
                "eventType": "teamMemberRemoved",
                "team": {"id": "team_id_1", "name": "new_team_name"},
            },
            members_removed=[
                ChannelAccount(
                    id="123",
                    name="test_user",
                    aad_object_id="asdfqwerty",
                    role="tester",
                )
            ],
            channel_id=Channels.ms_teams,
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_conversation_update_activity"
        assert bot.record[1] == "on_teams_members_removed"

    async def test_on_signin_verify_state(self):
        # arrange
        activity = Activity(type=ActivityTypes.invoke, name="signin/verifyState")

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_invoke_activity"
        assert bot.record[1] == "on_teams_signin_verify_state"

    async def test_on_file_consent_accept_activity(self):
        # arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="fileConsent/invoke",
            value={"action": "accept"},
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 3
        assert bot.record[0] == "on_invoke_activity"
        assert bot.record[1] == "on_teams_file_consent"
        assert bot.record[2] == "on_teams_file_consent_accept"

    async def test_on_file_consent_decline_activity(self):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="fileConsent/invoke",
            value={"action": "decline"},
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 3
        assert bot.record[0] == "on_invoke_activity"
        assert bot.record[1] == "on_teams_file_consent"
        assert bot.record[2] == "on_teams_file_consent_decline"

    async def test_on_file_consent_bad_action_activity(self):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="fileConsent/invoke",
            value={"action": "bad_action"},
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_invoke_activity"
        assert bot.record[1] == "on_teams_file_consent"

    async def test_on_teams_o365_connector_card_action(self):
        # arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="actionableMessage/executeAction",
            value={"body": "body_here", "actionId": "action_id_here"},
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_invoke_activity"
        assert bot.record[1] == "on_teams_o365_connector_card_action"

    async def test_on_app_based_link_query(self):
        # arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="composeExtension/query",
            value={"url": "http://www.test.com"},
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_invoke_activity"
        assert bot.record[1] == "on_teams_messaging_extension_query"

    async def test_on_teams_messaging_extension_bot_message_preview_edit_activity(self):
        # Arrange

        activity = Activity(
            type=ActivityTypes.invoke,
            name="composeExtension/submitAction",
            value={
                "data": {"key": "value"},
                "context": {"theme": "dark"},
                "commandId": "test_command",
                "commandContext": "command_context_test",
                "botMessagePreviewAction": "edit",
                "botActivityPreview": [{"id": "activity123"}],
                "messagePayload": {"id": "payloadid"},
            },
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 3
        assert bot.record[0] == "on_invoke_activity"
        assert bot.record[1] == "on_teams_messaging_extension_submit_action_dispatch"
        assert bot.record[2] == "on_teams_messaging_extension_bot_message_preview_edit"

    async def test_on_teams_messaging_extension_bot_message_send_activity(self):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="composeExtension/submitAction",
            value={
                "data": {"key": "value"},
                "context": {"theme": "dark"},
                "commandId": "test_command",
                "commandContext": "command_context_test",
                "botMessagePreviewAction": "send",
                "botActivityPreview": [{"id": "123"}],
                "messagePayload": {"id": "abc"},
            },
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 3
        assert bot.record[0] == "on_invoke_activity"
        assert bot.record[1] == "on_teams_messaging_extension_submit_action_dispatch"
        assert bot.record[2] == "on_teams_messaging_extension_bot_message_preview_send"

    async def test_on_teams_messaging_extension_bot_message_send_activity_with_none(
        self,
    ):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="composeExtension/submitAction",
            value={
                "data": {"key": "value"},
                "context": {"theme": "dark"},
                "commandId": "test_command",
                "commandContext": "command_context_test",
                "botMessagePreviewAction": None,
                "botActivityPreview": [{"id": "test123"}],
                "messagePayload": {"id": "payloadid123"},
            },
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 3
        assert bot.record[0] == "on_invoke_activity"
        assert bot.record[1] == "on_teams_messaging_extension_submit_action_dispatch"
        assert bot.record[2] == "on_teams_messaging_extension_submit_action"

    async def test_on_teams_messaging_extension_bot_message_send_activity_with_empty_string(
        self,
    ):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="composeExtension/submitAction",
            value={
                "data": {"key": "value"},
                "context": {"theme": "dark"},
                "commandId": "test_command",
                "commandContext": "command_context_test",
                "botMessagePreviewAction": "",
                "botActivityPreview": [Activity().serialize()],
                "messagePayload": MessageActionsPayload().serialize(),
            },
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 3
        assert bot.record[0] == "on_invoke_activity"
        assert bot.record[1] == "on_teams_messaging_extension_submit_action_dispatch"
        assert bot.record[2] == "on_teams_messaging_extension_submit_action"

    async def test_on_teams_messaging_extension_fetch_task(self):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="composeExtension/fetchTask",
            value={
                "data": {"key": "value"},
                "context": {"theme": "dark"},
                "commandId": "test_command",
                "commandContext": "command_context_test",
                "botMessagePreviewAction": "message_action",
                "botActivityPreview": [{"id": "123"}],
                "messagePayload": {"id": "abc123"},
            },
        )
        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_invoke_activity"
        assert bot.record[1] == "on_teams_messaging_extension_fetch_task"

    async def test_on_teams_messaging_extension_configuration_query_settings_url(self):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="composeExtension/querySettingUrl",
            value={
                "commandId": "test_command",
                "parameters": [],
                "messagingExtensionQueryOptions": {"skip": 1, "count": 1},
                "state": "state_string",
            },
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_invoke_activity"
        assert (
            bot.record[1]
            == "on_teams_messaging_extension_configuration_query_settings_url"
        )

    async def test_on_teams_messaging_extension_configuration_setting(self):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="composeExtension/setting",
            value={"key": "value"},
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_invoke_activity"
        assert bot.record[1] == "on_teams_messaging_extension_configuration_setting"

    async def test_on_teams_messaging_extension_card_button_clicked(self):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="composeExtension/onCardButtonClicked",
            value={"key": "value"},
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_invoke_activity"
        assert bot.record[1] == "on_teams_messaging_extension_card_button_clicked"

    async def test_on_teams_task_module_fetch(self):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="task/fetch",
            value={
                "data": {"key": "value"},
                "context": TaskModuleRequestContext().serialize(),
            },
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_invoke_activity"
        assert bot.record[1] == "on_teams_task_module_fetch"

    async def test_on_teams_task_module_submit(self):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="task/submit",
            value={
                "data": {"key": "value"},
                "context": TaskModuleRequestContext().serialize(),
            },
        )

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_invoke_activity"
        assert bot.record[1] == "on_teams_task_module_submit"

    async def test_on_end_of_conversation_activity(self):
        activity = Activity(type=ActivityTypes.end_of_conversation)

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        assert len(bot.record) == 1
        assert bot.record[0] == "on_end_of_conversation_activity"

    async def test_typing_activity(self):
        activity = Activity(type=ActivityTypes.typing)

        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        assert len(bot.record) == 1
        assert bot.record[0] == "on_typing_activity"
