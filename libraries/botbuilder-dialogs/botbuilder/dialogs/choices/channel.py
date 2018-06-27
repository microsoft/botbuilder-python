# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import BotContext


class Channels:
    """INTERNAL: Accessible through the Channel class via `Channel.channels`."""
    facebook = 'facebook'
    skype = 'skype'
    msteams = 'msteams'
    telegram = 'telegram'
    kik = 'kik'
    email = 'email'
    slack = 'slack'
    groupme = 'groupme'
    sms = 'sms'
    emulator = 'emulator'
    directline = 'directline'
    webchat = 'webchat'
    console = 'console'
    cortana = 'cortana'


class Channel:
    channels = Channels

    @staticmethod
    def supports_suggested_actions(channel_id: str, button_count: int = 100) -> bool:
        """
        Checks if a Bot Framework supported channel supports a certain number of suggestedActions.
        :param channel_id:
        :param button_count:
        :return:
        """
        if hasattr(Channels, channel_id):
            if channel_id == Channels.facebook or channel_id == Channels.skype:
                return button_count <= 10
            if channel_id == Channels.kik:
                return button_count <= 20
            if channel_id == Channels.slack or channel_id == Channels.telegram or channel_id == Channels.emulator:
                return button_count <= 100
        else:
            return False

    @staticmethod
    def supports_card_actions(channel_id: str, button_count: int = 100) -> bool:
        """
        Checks if a Bot Framework supported channel supports a certain number of card actions.
        :param channel_id:
        :param button_count:
        :return:
        """
        if hasattr(Channels, channel_id):
            if channel_id == Channels.facebook or channel_id == Channels.skype or channel_id == Channels.msteams:
                return button_count <= 3
            if (channel_id == Channels.slack or channel_id == Channels.directline or channel_id == Channels.emulator or
                    channel_id == Channels.webchat or channel_id == Channels.cortana):
                return button_count <= 100
        else:
            return False

    @staticmethod
    def has_message_feed(channel_id: str) -> bool:
        """
        :param channel_id:
        :return:
        """
        if channel_id == Channels.cortana:
            return False
        else:
            return True

    @staticmethod
    def max_action_title_length(channel_id: str) -> int:
        """
        :param channel_id:
        :return:
        """
        return 20

    @staticmethod
    def get_channel_id(context: BotContext) -> str:
        """
        :param context:
        :return:
        """
        return context.activity.channel_id
