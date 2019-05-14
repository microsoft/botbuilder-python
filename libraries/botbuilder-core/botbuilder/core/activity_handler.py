import asyncio
from botbuilder.schema import ( 
                            ActivityTypes, 
                            ChannelAccount 
                            )
from .turn_context import TurnContext


class ActivityHandler:

    async def on_turn(self, turn_context: TurnContext):
        if turn_context is None:
            raise TypeError('ActivityHandler.on_turn(): turn_context cannot be None.')

        if hasattr(turn_context, 'activity') and turn_context.activity is None:
            raise TypeError('ActivityHandler.on_turn(): turn_context must have a non-None activity.')

        if hasattr(turn_context.activity, 'type') and turn_context.activity.type is None:
            raise TypeError('ActivityHandler.on_turn(): turn_context activity must have a non-None type.')

        if turn_context.activity.type == ActivityTypes.message:
            await self.on_message_activity(turn_context)
        elif turn_context.activity.type == ActivityTypes.conversation_update:
            await self.on_conversation_update_activity(turn_context)
        elif turn_context.activity.type == ActivityTypes.event:
            await self.on_event_activity(turn_context)
        else:
            await self.on_unrecognized_activity_type(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        return

    async def on_conversation_update_activity(self, turn_context: TurnContext):
        if turn_context.activity.members_added is not None and len(turn_context.activity.members_added) > 0:
            return await self.on_members_added_activity(turn_context.activity.members_added, turn_context)
        elif turn_context.activity.members_removed is not None and len(turn_context.activity.members_removed) > 0:
            return await self.on_members_removed_activity(turn_context.activity.members_removed, turn_context)
        return

    async def on_members_added_activity(self, members_added: ChannelAccount, turn_context: TurnContext):
        return

    async def on_members_removed_activity(self, members_removed: ChannelAccount, turn_context: TurnContext):
        return

    async def on_event_activity(self, turn_context: TurnContext):
        if turn_context.activity.name == 'tokens/response':
            return await self.on_token_response_event(turn_context)

        return await self.on_event(turn_context)

    async def on_token_response_event(self, turn_context: TurnContext):
        return

    async def on_event(self, turn_context: TurnContext):
        return

    async def on_unrecognized_activity_type(self, turn_context: TurnContext):
        return
