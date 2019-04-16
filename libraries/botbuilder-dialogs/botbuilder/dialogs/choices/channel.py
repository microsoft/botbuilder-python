# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import TurnContext
from botframework.connector import Channels


class Channel(object):
    """
    Methods for determining channel specific functionality.
    """

    @staticmethod
    def supports_suggested_actions(channel_id: str, button_cnt: int = 100) -> bool:
        """Determine if a number of Suggested Actions are supported by a Channel.

        Args:
            channel_id (str): The Channel to check the if Suggested Actions are supported in.
            button_cnt (int, optional): Defaults to 100. The number of Suggested Actions to check for the Channel.

        Returns:
            bool: True if the Channel supports the button_cnt total Suggested Actions, False if the Channel does not support that number of Suggested Actions.
        """

        max_actions = {
            # https://developers.facebook.com/docs/messenger-platform/send-messages/quick-replies
            Channels.Facebook: 10,
            Channels.Skype: 10,
            # https://developers.line.biz/en/reference/messaging-api/#items-object
            Channels.Line: 13,
            # https://dev.kik.com/#/docs/messaging#text-response-object
            Channels.Kik: 20,
            Channels.Telegram: 100,
            Channels.Slack: 100,
            Channels.Emulator: 100,
            Channels.Directline: 100,
            Channels.Webchat: 100,
        }
        return button_cnt <= max_actions[channel_id] if channel_id in max_actions else False

    @staticmethod
    def supports_card_actions(channel_id: str, button_cnt: int = 100) -> bool:
        """Determine if a number of Card Actions are supported by a Channel.

        Args:
            channel_id (str): The Channel to check if the Card Actions are supported in.
            button_cnt (int, optional): Defaults to 100. The number of Card Actions to check for the Channel.

        Returns:
            bool: True if the Channel supports the button_cnt total Card Actions, False if the Channel does not support that number of Card Actions.
        """

        max_actions = {
            Channels.Facebook: 3,
            Channels.Skype: 3,
            Channels.Msteams: 3,
            Channels.Line: 99,
            Channels.Slack: 100,
            Channels.Emulator: 100,
            Channels.Directline: 100,
            Channels.Webchat: 100,
            Channels.Cortana: 100,
        }
        return button_cnt <= max_actions[channel_id] if channel_id in max_actions else False

    @staticmethod
    def has_message_feed(channel_id: str) -> bool:
        """Determine if a Channel has a Message Feed.

        Args:
            channel_id (str): The Channel to check for Message Feed.

        Returns:
            bool: True if the Channel has a Message Feed, False if it does not.
        """

        return False if channel_id == Channels.Cortana else True

    @staticmethod
    def max_action_title_length(channel_id: str) -> int:
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

        if turn_context.activity.channelId is None:
            return ""
        else:
            return turn_context.activity.channelId
