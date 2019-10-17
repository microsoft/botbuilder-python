from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ConversationAccount,
    ChannelAccount,
)
from botbuilder.core import TurnContext
from botbuilder.core.adapters import TestAdapter


class TestUtilities:
    @staticmethod
    def create_empty_context():
        adapter = TestAdapter()
        activity = Activity(
            type=ActivityTypes.message,
            channel_id="EmptyContext",
            conversation=ConversationAccount(id="test"),
            from_property=ChannelAccount(id="empty@empty.context.org"),
        )
        context = TurnContext(adapter, activity)

        return context
