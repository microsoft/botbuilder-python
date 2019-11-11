# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import MessageFactory, TurnContext
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema.teams import ChannelInfo, TeamInfo, TeamsChannelAccount


class ConversationUpdateBot(TeamsActivityHandler):
    async def on_teams_channel_created_activity(
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        return await turn_context.send_activity(
            MessageFactory.text(
                f"The new channel is {channel_info.name}. The channel id is {channel_info.id}"
            )
        )

    async def on_teams_channel_deleted_activity(
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        return await turn_context.send_activity(
            MessageFactory.text(f"The deleted channel is {channel_info.name}")
        )

    async def on_teams_channel_renamed_activity(
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        return await turn_context.send_activity(
            MessageFactory.text(f"The new channel name is {channel_info.name}")
        )

    async def on_teams_team_renamed_activity(
        self, team_info: TeamInfo, turn_context: TurnContext
    ):
        return await turn_context.send_activity(
            MessageFactory.text(f"The new team name is {team_info.name}")
        )

    async def on_teams_members_added_activity(
        self, teams_members_added: [TeamsChannelAccount], turn_context: TurnContext
    ):
        for member in teams_members_added:
            await turn_context.send_activity(
                MessageFactory.text(f"Welcome your new team member {member.id}")
            )
        return

    async def on_teams_members_removed_activity(
        self, teams_members_removed: [TeamsChannelAccount], turn_context: TurnContext
    ):
        for member in teams_members_removed:
            await turn_context.send_activity(
                MessageFactory.text(f"Say goodbye to your team member {member.id}")
            )
        return
