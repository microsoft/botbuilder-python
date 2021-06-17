from http import HTTPStatus
from typing import List

import aiounittest
from botframework.connector import ConnectorClient
from botframework.connector.auth import AppCredentials

from botbuilder.core import ActivityHandler, BotAdapter, TurnContext
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    ConversationReference,
    MessageReaction,
    ResourceResponse,
)


class TestingActivityHandler(ActivityHandler):
    __test__ = False

    def __init__(self):
        self.record: List[str] = []

    async def on_message_activity(self, turn_context: TurnContext):
        self.record.append("on_message_activity")
        return await super().on_message_activity(turn_context)

    async def on_members_added_activity(
        self, members_added: ChannelAccount, turn_context: TurnContext
    ):
        self.record.append("on_members_added_activity")
        return await super().on_members_added_activity(members_added, turn_context)

    async def on_members_removed_activity(
        self, members_removed: ChannelAccount, turn_context: TurnContext
    ):
        self.record.append("on_members_removed_activity")
        return await super().on_members_removed_activity(members_removed, turn_context)

    async def on_message_reaction_activity(self, turn_context: TurnContext):
        self.record.append("on_message_reaction_activity")
        return await super().on_message_reaction_activity(turn_context)

    async def on_reactions_added(
        self, message_reactions: List[MessageReaction], turn_context: TurnContext
    ):
        self.record.append("on_reactions_added")
        return await super().on_reactions_added(message_reactions, turn_context)

    async def on_reactions_removed(
        self, message_reactions: List[MessageReaction], turn_context: TurnContext
    ):
        self.record.append("on_reactions_removed")
        return await super().on_reactions_removed(message_reactions, turn_context)

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

    async def on_installation_update(self, turn_context: TurnContext):
        self.record.append("on_installation_update")
        return await super().on_installation_update(turn_context)

    async def on_installation_update_add(self, turn_context: TurnContext):
        self.record.append("on_installation_update_add")
        return await super().on_installation_update_add(turn_context)

    async def on_installation_update_remove(self, turn_context: TurnContext):
        self.record.append("on_installation_update_remove")
        return await super().on_installation_update_remove(turn_context)

    async def on_unrecognized_activity_type(self, turn_context: TurnContext):
        self.record.append("on_unrecognized_activity_type")
        return await super().on_unrecognized_activity_type(turn_context)

    async def on_invoke_activity(self, turn_context: TurnContext):
        self.record.append("on_invoke_activity")
        if turn_context.activity.name == "some.random.invoke":
            return self._create_invoke_response()

        return await super().on_invoke_activity(turn_context)

    async def on_sign_in_invoke(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        self.record.append("on_sign_in_invoke")
        return


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


class TestInvokeAdapter(NotImplementedAdapter):
    def __init__(self, on_turn_error=None, activity: Activity = None):
        super().__init__(on_turn_error)

        self.activity = activity

    async def delete_activity(
        self, context: TurnContext, reference: ConversationReference
    ):
        raise NotImplementedError()

    async def send_activities(
        self, context: TurnContext, activities: List[Activity]
    ) -> List[ResourceResponse]:
        self.activity = next(
            (
                activity
                for activity in activities
                if activity.type == ActivityTypes.invoke_response
            ),
            None,
        )

        return []

    async def update_activity(self, context: TurnContext, activity: Activity):
        raise NotImplementedError()


class MockConnectorClient(ConnectorClient):
    def __init__(self):
        super().__init__(
            credentials=MockCredentials(), base_url="http://tempuri.org/whatever"
        )


class MockCredentials(AppCredentials):
    def get_access_token(self, force_refresh: bool = False) -> str:
        return "awesome"


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

    async def test_invoke(self):
        activity = Activity(type=ActivityTypes.invoke, name="some.random.invoke")

        adapter = TestInvokeAdapter()
        turn_context = TurnContext(adapter, activity)

        # Act
        bot = TestingActivityHandler()
        await bot.on_turn(turn_context)

        assert len(bot.record) == 1
        assert bot.record[0] == "on_invoke_activity"
        assert adapter.activity.value.status == int(HTTPStatus.OK)

    async def test_invoke_should_not_match(self):
        activity = Activity(type=ActivityTypes.invoke, name="should.not.match")

        adapter = TestInvokeAdapter()
        turn_context = TurnContext(adapter, activity)

        # Act
        bot = TestingActivityHandler()
        await bot.on_turn(turn_context)

        assert len(bot.record) == 1
        assert bot.record[0] == "on_invoke_activity"
        assert adapter.activity.value.status == int(HTTPStatus.NOT_IMPLEMENTED)

    async def test_on_end_of_conversation_activity(self):
        activity = Activity(type=ActivityTypes.end_of_conversation)

        adapter = TestInvokeAdapter()
        turn_context = TurnContext(adapter, activity)

        # Act
        bot = TestingActivityHandler()
        await bot.on_turn(turn_context)

        assert len(bot.record) == 1
        assert bot.record[0] == "on_end_of_conversation_activity"

    async def test_typing_activity(self):
        activity = Activity(type=ActivityTypes.typing)

        adapter = TestInvokeAdapter()
        turn_context = TurnContext(adapter, activity)

        # Act
        bot = TestingActivityHandler()
        await bot.on_turn(turn_context)

        assert len(bot.record) == 1
        assert bot.record[0] == "on_typing_activity"

    async def test_on_installation_update(self):
        activity = Activity(type=ActivityTypes.installation_update)

        adapter = TestInvokeAdapter()
        turn_context = TurnContext(adapter, activity)

        # Act
        bot = TestingActivityHandler()
        await bot.on_turn(turn_context)

        assert len(bot.record) == 1
        assert bot.record[0] == "on_installation_update"

    async def test_on_installation_update_add(self):
        activity = Activity(type=ActivityTypes.installation_update, action="add")

        adapter = TestInvokeAdapter()
        turn_context = TurnContext(adapter, activity)

        # Act
        bot = TestingActivityHandler()
        await bot.on_turn(turn_context)

        assert len(bot.record) == 2
        assert bot.record[0] == "on_installation_update"
        assert bot.record[1] == "on_installation_update_add"

    async def test_on_installation_update_add_upgrade(self):
        activity = Activity(
            type=ActivityTypes.installation_update, action="add-upgrade"
        )

        adapter = TestInvokeAdapter()
        turn_context = TurnContext(adapter, activity)

        # Act
        bot = TestingActivityHandler()
        await bot.on_turn(turn_context)

        assert len(bot.record) == 2
        assert bot.record[0] == "on_installation_update"
        assert bot.record[1] == "on_installation_update_add"

    async def test_on_installation_update_remove(self):
        activity = Activity(type=ActivityTypes.installation_update, action="remove")

        adapter = TestInvokeAdapter()
        turn_context = TurnContext(adapter, activity)

        # Act
        bot = TestingActivityHandler()
        await bot.on_turn(turn_context)

        assert len(bot.record) == 2
        assert bot.record[0] == "on_installation_update"
        assert bot.record[1] == "on_installation_update_remove"

    async def test_on_installation_update_remove_upgrade(self):
        activity = Activity(
            type=ActivityTypes.installation_update, action="remove-upgrade"
        )

        adapter = TestInvokeAdapter()
        turn_context = TurnContext(adapter, activity)

        # Act
        bot = TestingActivityHandler()
        await bot.on_turn(turn_context)

        assert len(bot.record) == 2
        assert bot.record[0] == "on_installation_update"
        assert bot.record[1] == "on_installation_update_remove"
