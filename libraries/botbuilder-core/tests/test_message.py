# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    ConversationAccount,
)


class TestMessage:
    @staticmethod
    def message(id: str = "1234") -> Activity:  # pylint: disable=invalid-name
        return Activity(
            type=ActivityTypes.message,
            id=id,
            text="test",
            from_property=ChannelAccount(id="user", name="User Name"),
            recipient=ChannelAccount(id="bot", name="Bot Name"),
            conversation=ConversationAccount(id="convo", name="Convo Name"),
            channel_id="UnitTest",
            service_url="https://example.org",
        )
