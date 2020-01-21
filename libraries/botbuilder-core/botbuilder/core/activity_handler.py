# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import List

from botbuilder.schema import ActivityTypes, ChannelAccount, MessageReaction
from .turn_context import TurnContext


class ActivityHandler:
    async def on_turn(self, turn_context: TurnContext):
    """ Called by the adapter (for example, :class:`BotFrameworkAdapter`) at runtime 
    in order to process an inbound :class:`botbuilder.schema.Activity`.
        
        :param turn_context: The context object for this turn
        :type turn_context: :class:`TurnContext`
        
        :returns: A task that represents the work queued to execute
        
        .. remarks::
            It calls other methods in this class based on the type of the activity to
            process, which allows a derived class to provide type-specific logic in a controlled way.
            In a derived class, override this method to add logic that applies to all activity types.
            
            .. note::
                - Add logic to apply before the type-specific logic and before the call to the base class `OnTurnAsync` method.
                - Add logic to apply after the type-specific logic after the call to the base class `OnTurnAsync` method.
    """
        if turn_context is None:
            raise TypeError("ActivityHandler.on_turn(): turn_context cannot be None.")

        if hasattr(turn_context, "activity") and turn_context.activity is None:
            raise TypeError(
                "ActivityHandler.on_turn(): turn_context must have a non-None activity."
            )

        if (
            hasattr(turn_context.activity, "type")
            and turn_context.activity.type is None
        ):
            raise TypeError(
                "ActivityHandler.on_turn(): turn_context activity must have a non-None type."
            )

        if turn_context.activity.type == ActivityTypes.message:
            await self.on_message_activity(turn_context)
        elif turn_context.activity.type == ActivityTypes.conversation_update:
            await self.on_conversation_update_activity(turn_context)
        elif turn_context.activity.type == ActivityTypes.message_reaction:
            await self.on_message_reaction_activity(turn_context)
        elif turn_context.activity.type == ActivityTypes.event:
            await self.on_event_activity(turn_context)
        elif turn_context.activity.type == ActivityTypes.end_of_conversation:
            await self.on_end_of_conversation_activity(turn_context)
        else:
            await self.on_unrecognized_activity_type(turn_context)

    async def on_message_activity(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        """Override this method in a derived class to provide logic specific to activities, 
        such as the conversational logic.
        
        :param turn_context: The context object for this turn
        :type turn_context: :class:`TurnContext`

        :returns: A task that represents the work queued to execute

        """
        return

    async def on_conversation_update_activity(self, turn_context: TurnContext):
        """Invoked when a conversation update activity is received from the channel when the base behavior of
        `OnTurnAsync` is used.
        Conversation update activities are useful when it comes to responding to users being added to or removed from the conversation.
        For example, a bot could respond to a user being added by greeting the user.
        By default, this method calls :meth:`ActivityHandler.on_members_added_activity()` if any users have been added or 
        :meth:`ActivityHandler.on_members_removed_activity()` if any users have been removed. 
        The method checks the member ID so that it only responds to updates regarding members other than the bot itself.
        
        :param turn_context: The context object for this turn
        :type turn_context: :class:`TurnContext`
        :returns: A task that represents the work queued to execute

        .. remarks::
            When the :meth:'ActivityHandler.on_turn()` method receives a conversation update activity, it calls this method.
            If the conversation update activity indicates that members other than the bot joined the conversation, 
            it calls the  :meth:`ActivityHandler.on_members_added_activity()` method.
            If the conversation update activity indicates that members other than the bot left the conversation, 
            it calls the  :meth:`ActivityHandler.on_members_removed_activity()`  method.
            In a derived class, override this method to add logic that applies to all conversation update activities.
            Add logic to apply before the member added or removed logic before the call to this base class method.
        """
        if (
            turn_context.activity.members_added is not None
            and turn_context.activity.members_added
        ):
            return await self.on_members_added_activity(
                turn_context.activity.members_added, turn_context
            )
        if (
            turn_context.activity.members_removed is not None
            and turn_context.activity.members_removed
        ):
            return await self.on_members_removed_activity(
                turn_context.activity.members_removed, turn_context
            )
        return

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):  # pylint: disable=unused-argument
        return

    async def on_members_removed_activity(
        self, members_removed: List[ChannelAccount], turn_context: TurnContext
    ):  # pylint: disable=unused-argument
        return

    async def on_message_reaction_activity(self, turn_context: TurnContext):
        if turn_context.activity.reactions_added is not None:
            await self.on_reactions_added(
                turn_context.activity.reactions_added, turn_context
            )

        if turn_context.activity.reactions_removed is not None:
            await self.on_reactions_removed(
                turn_context.activity.reactions_removed, turn_context
            )

    async def on_reactions_added(  # pylint: disable=unused-argument
        self, message_reactions: List[MessageReaction], turn_context: TurnContext
    ):
        return

    async def on_reactions_removed(  # pylint: disable=unused-argument
        self, message_reactions: List[MessageReaction], turn_context: TurnContext
    ):
        return

    async def on_event_activity(self, turn_context: TurnContext):
        if turn_context.activity.name == "tokens/response":
            return await self.on_token_response_event(turn_context)

        return await self.on_event(turn_context)

    async def on_token_response_event(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        return

    async def on_event(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        return

    async def on_end_of_conversation_activity(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        return

    async def on_unrecognized_activity_type(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        return
