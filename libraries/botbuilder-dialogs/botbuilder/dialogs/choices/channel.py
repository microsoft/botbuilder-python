# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import TurnContext
from botframework.connector import Channels


class Channel:
    """
    Methods for determining channel-specific functionality.
    """

    @staticmethod
    def supports_suggested_actions(channel_id: str, button_cnt: int = 100) -> bool:
        """Determine if a number of Suggested Actions are supported by a Channel.

        Args:
            channel_id (str): The Channel to check the if Suggested Actions are supported in.
            button_cnt (int, optional): Defaults to 100. The number of Suggested Actions to check for the Channel.

        Returns:
            bool: True if the Channel supports the button_cnt total Suggested Actions, False if the Channel does not
             support that number of Suggested Actions.
        """

        max_actions = {
            # https://developers.facebook.com/docs/messenger-platform/send-messages/quick-replies
            Channels.facebook: 10,
            Channels.skype: 10,
            # https://developers.line.biz/en/reference/messaging-api/#items-object
            Channels.line: 13,
            # https://dev.kik.com/#/docs/messaging#text-response-object
            Channels.kik: 20,
            Channels.telegram: 100,
            Channels.emulator: 100,
            Channels.direct_line: 100,
            Channels.webchat: 100,
        }
        return (
            button_cnt <= max_actions[channel_id]
            if channel_id in max_actions
            else False
        )

    @staticmethod
    def supports_card_actions(channel_id: str, button_cnt: int = 100) -> bool:
        """Determine if a number of Card Actions are supported by a Channel.

        Args:
            channel_id (str): The Channel to check if the Card Actions are supported in.
            button_cnt (int, optional): Defaults to 100. The number of Card Actions to check for the Channel.

        Returns:
            bool: True if the Channel supports the button_cnt total Card Actions, False if the Channel does not support
             that number of Card Actions.
        """

        max_actions = {
            Channels.facebook: 3,
            Channels.skype: 3,
            Channels.ms_teams: 3,
            Channels.line: 99,
            Channels.slack: 100,
            Channels.telegram: 100,
            Channels.emulator: 100,
            Channels.direct_line: 100,
            Channels.webchat: 100,
        }
        return (
            button_cnt <= max_actions[channel_id]
            if channel_id in max_actions
            else False
        )

    @staticmethod
    def has_message_feed(_: str) -> bool:
        """Determine if a Channel has a Message Feed.

        Args:
            channel_id (str): The Channel to check for Message Feed.

        Returns:
            bool: True if the Channel has a Message Feed, False if it does not.
        """

        return True

    @staticmethod
    def max_action_title_length(  # pylint: disable=unused-argument
        channel_id: str,
    ) -> int:
        """Maximum length allowed for Action Titles.

        Args:
            channel_id (str): The Channel to determine Maximum Action Title Length.

        Returns:
            int: The total number of characters allowed for an Action Title on a specific Channel.
        """

        return 20

    @staticmethod
    def get_channel_id(turn_context: TurnContext) -> str:
        """Get the Channel Id from the current Activity on the Turn Context.

        Args:
            turn_context (TurnContext): The Turn Context to retrieve the Activity's Channel Id from.

        Returns:
            str: The Channel Id from the Turn Context's Activity.
        """

        if turn_context.activity.channel_id is None:
            return ""

        return turn_context.activity.channel_id
