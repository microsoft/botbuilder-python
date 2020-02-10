# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import List

from botbuilder.schema import ActivityTypes, ChannelAccount, MessageReaction
from .turn_context import TurnContext


class ActivityHandler:
    """
    Class to handle actviities and intended for subclassing.

    .. remarks::
        Derive from this class to plug in code to handle particular activity types.
        Pre- and post-processing of activities can be added by calling the base class implementation
        from the derived class.
    """
    async def on_turn(self, turn_context: TurnContext):
        """
        Called by the adapter (for example, :class:`BotFrameworkAdapter`) at runtime
        in order to process an inbound :class:`botbuilder.schema.Activity`.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`botbuilder.core.TurnContext`

        :returns: A task that represents the work queued to execute

        .. remarks::
            It calls other methods in this class based on the type of the activity to
            process, which allows a derived class to provide type-specific logic in a controlled way.
            In a derived class, override this method to add logic that applies to all activity types.
            Also
            - Add logic to apply before the type-specific logic and before calling :meth:`ActivityHandler.on_turn()`.
            - Add logic to apply after the type-specific logic after calling :meth:`ActivityHandler.on_turn()`.
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
        """
        Override this method in a derived class to provide logic specific to activities,
        such as the conversational logic.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`botbuilder.core.TurnContext`

        :returns: A task that represents the work queued to execute
        """
        return

    async def on_conversation_update_activity(self, turn_context: TurnContext):
        """
        Invoked when a conversation update activity is received from the channel when the base behavior of
        :meth:`ActivityHandler.on_turn()` is used.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`botbuilder.core.TurnContext`

        :returns: A task that represents the work queued to execute

        .. remarks::
            When the :meth:'ActivityHandler.on_turn()` method receives a conversation update activity, it calls this
            method.

            If the conversation update activity indicates that members other than the bot joined the conversation,

            it calls the  :meth:`on_members_added_activity()` method.

            If the conversation update activity indicates that members other than the bot left the conversation,

            it calls the  :meth:`on_members_removed_activity()`  method.

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
        """
        Override this method in a derived class to provide logic for when members other than the bot join
        the conversation. You can add your bot's welcome logic.

        :param members_added: A list of all the members added to the conversation
        :type members_added: :class:`typing.List`
        :param turn_context: The context object for this turn
        :type turn_context: :class:`botbuilder.core.TurnContext`

        :returns: A task that represents the work queued to execute

        .. remarks::
            When the :meth:'ActivityHandler.on_conversation_update_activity()` method receives a conversation
            update activity that indicates
            one or more users other than the bot are joining the conversation, it calls this method.
        """
        return

    async def on_members_removed_activity(
        self, members_removed: List[ChannelAccount], turn_context: TurnContext
    ):  # pylint: disable=unused-argument
        """
        Override this method in a derived class to provide logic for when members other than the bot leave
        the conversation.  You can add your bot's good-bye logic.

        :param members_added: A list of all the members removed from the conversation
        :type members_added: :class:`typing.List`
        :param turn_context: The context object for this turn
        :type turn_context: :class:`botbuilder.core.TurnContext`

        :returns: A task that represents the work queued to execute

        .. remarks::
            When the :meth:'ActivityHandler.on_conversation_update_activity()` method receives a conversation
            update activity that indicates one or more users other than the bot are leaving the conversation,
            it calls this method.
        """

        return

    async def on_message_reaction_activity(self, turn_context: TurnContext):
        """
        Invoked when an event activity is received from the connector when the base behavior of
        :meth:'ActivityHandler.on_turn()` is used.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`botbuilder.core.TurnContext`

        :returns: A task that represents the work queued to execute

        .. remarks::
            Message reactions correspond to the user adding a 'like' or 'sad' etc. (often an emoji) to a previously
            sent activity.

            Message reactions are only supported by a few channels. The activity that the message reaction corresponds
            to is indicated in the reply to Id property. The value of this property is the activity id of a previously
            sent activity given back to the bot as the response from a send call.
            When the :meth:'ActivityHandler.on_turn()` method receives a message reaction activity, it calls this
            method.

            If the message reaction indicates that reactions were added to a message, it calls
            :meth:'ActivityHandler.on_reaction_added().
            If the message reaction indicates that reactions were removed from a message, it calls
            :meth:'ActivityHandler.on_reaction_removed().

            In a derived class, override this method to add logic that applies to all message reaction activities.
            Add logic to apply before the reactions added or removed logic before the call to the this base class
            method.
            Add logic to apply after the reactions added or removed logic after the call to the this base class method.
        """
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
        """
        Override this method in a derived class to provide logic for when reactions to a previous activity
        are added to the conversation.

        :param message_reactions: The list of reactions added
        :type message_reactions: :class:`typing.List`
        :param turn_context: The context object for this turn
        :type turn_context: :class:`botbuilder.core.TurnContext`

        :returns: A task that represents the work queued to execute

        .. remarks::
            Message reactions correspond to the user adding a 'like' or 'sad' etc. (often an emoji)
            to a previously sent message on the conversation. Message reactions are supported by only a few channels.

            The activity that the message is in reaction to is identified by the activity's reply to Id property.
            The value of this property is the activity ID of a previously sent activity. When the bot sends an activity,
            the channel assigns an ID to it, which is available in the resource response Id of the result.
        """
        return

    async def on_reactions_removed(  # pylint: disable=unused-argument
        self, message_reactions: List[MessageReaction], turn_context: TurnContext
    ):
        """
        Override this method in a derived class to provide logic for when reactions to a previous activity
        are removed from the conversation.

        :param message_reactions: The list of reactions removed
        :type message_reactions: :class:`typing.List`
        :param turn_context: The context object for this turn
        :type turn_context: :class:`botbuilder.core.TurnContext`

        :returns: A task that represents the work queued to execute

        .. remarks::
            Message reactions correspond to the user adding a 'like' or 'sad' etc. (often an emoji)
            to a previously sent message on the conversation. Message reactions are supported by only a few channels.

            The activity that the message is in reaction to is identified by the activity's reply to Id property.
            The value of this property is the activity ID of a previously sent activity. When the bot sends an activity,
            the channel assigns an ID to it, which is available in the resource response Id of the result.
        """
        return

    async def on_event_activity(self, turn_context: TurnContext):
        """
        Called when an event activity is received from the connector when the base behavior of
        :meth:'ActivityHandler.on_turn()` is used.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`botbuilder.core.TurnContext`

        :returns: A task that represents the work queued to execute

        .. remarks::
            When the :meth:'ActivityHandler.on_turn()` method receives an event activity, it calls this method.
            If the activity name is `tokens/response`, it calls :meth:'ActivityHandler.on_token_response_event()`;
            otherwise, it calls :meth:'ActivityHandler.on_event()`.

            In a derived class, override this method to add logic that applies to all event activities.
            Add logic to apply before the specific event-handling logic before the call to this base class method.
            Add logic to apply after the specific event-handling logic after the call to this base class method.

            Event activities communicate programmatic information from a client or channel to a bot.
            The meaning of an event activity is defined by the event activity name property, which is meaningful within
            the scope of a channel.
        """
        if turn_context.activity.name == "tokens/response":
            return await self.on_token_response_event(turn_context)

        return await self.on_event(turn_context)

    async def on_token_response_event(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        """
        Called when a `tokens/response` event is received when the base behavior of
        :meth:'ActivityHandler.on_event_activity()` is used.
        If using an `oauth_prompt`, override this method to forward this activity to the current dialog.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`botbuilder.core.TurnContext`

        :returns: A task that represents the work queued to execute

        .. remarks::
            When the :meth:'ActivityHandler.on_event()` method receives an event with an activity name of
            `tokens/response`, it calls this method. If your bot uses an `oauth_prompt`, forward the incoming
            activity to the current dialog.
        """
        return

    async def on_event(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        """
        Invoked when an event other than `tokens/response` is received when the base behavior of
        :meth:'ActivityHandler.on_event_activity()` is used.


        :param turn_context: The context object for this turn
        :type turn_context: :class:`botbuilder.core.TurnContext`

        :returns: A task that represents the work queued to execute

        .. remarks::
            When the :meth:'ActivityHandler.on_event_activity()` is used method receives an event with an
            activity name other than `tokens/response`, it calls this method.
            This method could optionally be overridden if the bot is meant to handle miscellaneous events.
        """
        return

    async def on_end_of_conversation_activity(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        """
        Invoked when a conversation end activity is received from the channel.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`botbuilder.core.TurnContext`
        :returns: A task that represents the work queued to execute
        """
        return

    async def on_unrecognized_activity_type(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        """
        Called  when an activity other than a message, conversation update, or event is received when the base
        behavior of :meth:`ActivityHandler.on_turn()` is used.
        If overridden, this method could potentially respond to any of the other activity types.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`botbuilder.core.TurnContext`

        :returns: A task that represents the work queued to execute

        .. remarks::
            When the :meth:`ActivityHandler.on_turn()` method receives an activity that is not a message,
            conversation update, message reaction, or event activity, it calls this method.
        """
        return
