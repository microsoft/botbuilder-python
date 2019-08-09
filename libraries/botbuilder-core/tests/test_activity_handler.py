from typing import List

import aiounittest
from botbuilder.core import ActivityHandler, BotAdapter, TurnContext
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    ConversationReference,
    MessageReaction,
)


class TestingActivityHandler(ActivityHandler):
    def __init__(self):
        self.record: List[str] = []

    async def on_message_activity(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        self.record.append("on_message_activity")
        return

    async def on_members_added_activity(  # pylint: disable=unused-argument
        self, members_added: ChannelAccount, turn_context: TurnContext
    ):
        self.record.append("on_members_added_activity")
        return

    async def on_members_removed_activity(  # pylint: disable=unused-argument
        self, members_removed: ChannelAccount, turn_context: TurnContext
    ):
        self.record.append("on_members_removed_activity")
        return

    async def on_message_reaction_activity(
        self, turn_context: TurnContext
    ):  # pylint: disable=unused-argument
        self.record.append("on_message_reaction_activity")
        return

    async def on_reactions_added(  # pylint: disable=unused-argument
        self, message_reactions: List[MessageReaction], turn_context: TurnContext
    ):
        self.record.append("on_reactions_added")
        return

    async def on_reactions_removed(  # pylint: disable=unused-argument
        self, message_reactions: List[MessageReaction], turn_context: TurnContext
    ):
        self.record.append("on_reactions_removed")
        return

    async def on_token_response_event(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        self.record.append("on_token_response_event")
        return

    async def on_event(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        self.record.append("on_event")
        return

    async def on_unrecognized_activity_type(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        self.record.append("on_unrecognized_activity_type")
        return


class NotImplementedAdapter(BotAdapter):
    async def delete_activity(
        self, context: TurnContext, reference: ConversationReference
    ):
        raise NotImplementedError()

    async def send_activities(self, context: TurnContext, activities: List[Activity]):
        raise NotImplementedError()

    async def update_activity(self, context: TurnContext, activity: Activity):
        raise NotImplementedError()


class TestActivityHandler(aiounittest.AsyncTestCase):
    async def test_message_reaction(self):
        # Note the code supports multiple adds and removes in the same activity though
        # a channel may decide to send separate activities for each. For example, Teams
        # sends separate activities each with a single add and a single remove.

        # Arrange
        activity = Activity(
            type=ActivityTypes.message_reaction,
            reactions_added=[MessageReaction(type="sad")],
            reactions_removed=[MessageReaction(type="angry")],
        )
        turn_context = TurnContext(NotImplementedAdapter(), activity)

        # Act
        bot = TestingActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        assert len(bot.record) == 3
        assert bot.record[0] == "on_message_reaction_activity"
        assert bot.record[1] == "on_reactions_added"
        assert bot.record[2] == "on_reactions_removed"
