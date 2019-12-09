# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from botbuilder.core import MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
from botbuilder.core.teams import TeamsActivityHandler, TeamsInfo

class RosterBot(TeamsActivityHandler):
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Hello and welcome!"
                )

    async def on_message_activity(
        self, turn_context: TurnContext
    ):
        await turn_context.send_activity(MessageFactory.text(f"Echo: {turn_context.activity.text}"))

        text = turn_context.activity.text.strip()
        if "members" in text:
            await self._show_members(turn_context)
        elif "channels" in text:
            await self._show_channels(turn_context)
        elif "details" in text:
            await self._show_details(turn_context)
        else:
            await turn_context.send_activity(MessageFactory.text(f"Invalid command. Type \"Show channels\" to see a channel list. Type \"Show members\" to see a list of members in a team. Type \"Show details\" to see team information."))

    async def _show_members(
        self, turn_context: TurnContext
    ):
        members = await TeamsInfo.get_team_members(turn_context)
        reply = MessageFactory.text(f"Total of {len(members)} members are currently in team")
        await turn_context.send_activity(reply)
        messages = list(map(lambda m: (f'{m.aad_object_id} --> {m.name} --> {m.user_principal_name}'), members))
        await self._send_in_batches(turn_context, messages)

    async def _show_channels(
        self, turn_context: TurnContext
    ):
        channels = await TeamsInfo.get_team_channels(turn_context)
        reply = MessageFactory.text(f"Total of {len(channels)} channels are currently in team")
        await turn_context.send_activity(reply)
        messages = list(map(lambda c: (f'{c.id} --> {c.name}'), channels))
        await self._send_in_batches(turn_context, messages)
        
    async def _show_details(self, turn_context: TurnContext):
        team_details = await TeamsInfo.get_team_details(turn_context)
        reply = MessageFactory.text(f"The team name is {team_details.name}. The team ID is {team_details.id}. The AADGroupID is {team_details.aad_group_id}.")
        await turn_context.send_activity(reply)    
        
    async def _send_in_batches(self, turn_context: TurnContext, messages: List[str]):
        batch = []
        for msg in messages:
            batch.append(msg)
            if len(batch) == 10:
                await turn_context.send_activity(MessageFactory.text("<br>".join(batch)))
                batch = []

        if len(batch) > 0:
            await turn_context.send_activity(MessageFactory.text("<br>".join(batch)))