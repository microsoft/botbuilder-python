# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
from typing import List
from botbuilder.core import MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
from botbuilder.core.teams import TeamsActivityHandler, TeamsInfo
from botbuilder.schema.teams import ChannelInfo, TeamInfo, TeamsChannelAccount, TeamsChannelData

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

        # TODO: mentions seem to not have a 'mentioned' property ... issue with Entity super classes
        #for e in turn_context.activity.entities:
        #    await turn_context.send_activity(MessageFactory.text(f"e: {e.serialize()}"))

        #mentions = TurnContext.get_mentions(turn_context.activity)
        #for mention in mentions:
        #    await turn_context.send_activity(MessageFactory.text(f"mention.serialize(): {mention.serialize()}"))

 
        # TODO: remove_recipient_mention currently crashes...
        #TurnContext.remove_recipient_mention(turn_context.activity)
        text = turn_context.activity.text.strip()
        if "members" in text:
            await self._show_members(turn_context)
        elif "channels" in text:
            await self._show_channels(turn_context)
        elif "details" in text:
            await self._show_details(turn_context)
        else:
            await turn_context.send_activity(MessageFactory.text(f"Invalid command. Type \"Show channels\" to see a channel list. Type \"Show members\" to see a list of members in a team."))

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
        channels = TeamsInfo.get_team_channels(turn_context)
        reply = MessageFactory.text(f"Total of {len(channels)} channels are currently in team")
        await turn_context.send_activity(reply)
        messages = list(map(lambda c: (f'{c.id} --> {c.name}'), channels))
        await self._send_in_batches(turn_context, messages)
        
    async def _show_details(self, turn_context: TurnContext):
        team_details = TeamsInfo.get_team_details(turn_context)
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