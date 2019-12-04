from typing import List

import aiounittest
from botbuilder.core import BotAdapter, TurnContext
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    ConversationReference,
    MessageReaction,
    ResourceResponse,
)
from botbuilder.schema.teams import (
    ChannelInfo,
    NotificationInfo,
    TeamInfo,
    TeamsChannelAccount,
    TeamsChannelData,
    TenantInfo,    
)
from botframework.connector import Channels
from .. import SimpleAdapter

class TestingTeamsActivityHandler(TeamsActivityHandler):
    def __init__(self):
        self.record: List[str] = []

    async def on_conversation_update_activity(self, turn_context: TurnContext):
        self.record.append("on_conversation_update_activity")
        return await super().on_conversation_update_activity(turn_context)

    async def on_teams_members_added_activity(self, teams_members_added: [TeamsChannelAccount], turn_context: TurnContext):
        self.record.append("on_teams_members_added_activity")
        return await super().on_teams_members_added_activity(teams_members_added, turn_context)
    
    async def on_teams_members_removed_activity(self, teams_members_removed: [TeamsChannelAccount], turn_context: TurnContext):
        self.record.append("on_teams_members_removed_activity")
        return await super().on_teams_members_removed_activity(teams_members_removed, turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        self.record.append("on_message_activity")
        return await super().on_message_activity(turn_context)

    async def on_token_response_event(self, turn_context: TurnContext):
        self.record.append("on_token_response_event")
        return await super().on_token_response_event(turn_context)

    async def on_event(self, turn_context: TurnContext):
        self.record.append("on_event")
        return await super().on_event(turn_context)

    async def on_unrecognized_activity_type(self, turn_context: TurnContext):
        self.record.append("on_unrecognized_activity_type")
        return await super().on_unrecognized_activity_type(turn_context)
    
    async def on_teams_channel_created_activity(
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        self.record.append("on_teams_channel_created_activity")
        return await super().on_teams_channel_created_activity(channel_info, team_info, turn_context)
    
    async def on_teams_channel_renamed_activity(
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        self.record.append("on_teams_channel_renamed_activity")
        return await super().on_teams_channel_renamed_activity(channel_info, team_info, turn_context)
    
    async def on_teams_channel_deleted_activity(
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        self.record.append("on_teams_channel_deleted_activity")
        return await super().on_teams_channel_renamed_activity(channel_info, team_info, turn_context)
    
    async def on_teams_team_renamed_activity(self, team_info: TeamInfo, turn_context: TurnContext):
        self.record.append("on_teams_team_renamed_activity")
        return await super().on_teams_team_renamed_activity(team_info, turn_context)

    async def on_invoke_activity(self, turn_context: TurnContext):
        self.record.append("on_invoke_activity")
        return await super().on_invoke_activity(turn_context)

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
        #arrange 
        activity = Activity(
            type = ActivityTypes.conversation_update,
            channel_data = {
                            "eventType": "channelCreated",
                            "channel": {
                                        "id": "asdfqwerty",
                                        "name" : "new_channel"
                                        }
                            },
            channel_id = Channels.ms_teams
        )

        turn_context = TurnContext(NotImplementedAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_conversation_update_activity"
        assert bot.record[1] == "on_teams_channel_created_activity"
    
    async def test_on_teams_channel_renamed_activity(self):
        #arrange 
        activity = Activity(
            type = ActivityTypes.conversation_update,
            channel_data = {
                            "eventType": "channelRenamed",
                            "channel": {
                                        "id": "asdfqwerty",
                                        "name" : "new_channel"
                                        }
                            },
            channel_id = Channels.ms_teams
        )

        turn_context = TurnContext(NotImplementedAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_conversation_update_activity"
        assert bot.record[1] == "on_teams_channel_renamed_activity"
    
    async def test_on_teams_channel_deleted_activity(self):
        #arrange 
        activity = Activity(
            type = ActivityTypes.conversation_update,
            channel_data = {
                            "eventType": "channelDeleted",
                            "channel": {
                                        "id": "asdfqwerty",
                                        "name" : "new_channel"
                                        }
                            },
            channel_id = Channels.ms_teams
        )

        turn_context = TurnContext(NotImplementedAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_conversation_update_activity"
        assert bot.record[1] == "on_teams_channel_deleted_activity"
    
    async def test_on_teams_team_renamed_activity(self):
        #arrange 
        activity = Activity(
            type = ActivityTypes.conversation_update,
            channel_data = {
                            "eventType": "teamRenamed",
                            "team": {
                                        "id": "team_id_1",
                                        "name" : "new_team_name"
                                        }
                            },
            channel_id = Channels.ms_teams
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
        #arrange 
        activity = Activity(
            type = ActivityTypes.conversation_update,
            channel_data = {
                            "eventType": "teamMemberAdded"
                            },
            members_added = [ChannelAccount(id="123", name="test_user", aad_object_id="asdfqwerty", role="tester")],
            channel_id = Channels.ms_teams
        )

        turn_context = TurnContext(NotImplementedAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_conversation_update_activity"
        assert bot.record[1] == "on_teams_members_added_activity"
    
    async def test_on_teams_members_removed_activity(self):
        #arrange 
        activity = Activity(
            type = ActivityTypes.conversation_update,
            channel_data = {
                            "eventType": "teamMemberRemoved"
                            },
            members_removed = [ChannelAccount(id="123", name="test_user", aad_object_id="asdfqwerty", role="tester")],
            channel_id = Channels.ms_teams
        )

        turn_context = TurnContext(NotImplementedAdapter(), activity)

        # Act
        bot = TestingTeamsActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 2
        assert bot.record[0] == "on_conversation_update_activity"
        assert bot.record[1] == "on_teams_members_removed_activity"