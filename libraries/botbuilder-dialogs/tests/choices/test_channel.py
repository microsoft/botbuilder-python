# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import unittest
from typing import List, Tuple

from botbuilder.core import BotFrameworkAdapter, TurnContext
from botbuilder.dialogs.choices import Channel
from botbuilder.schema import Activity
from botframework.connector import Channels


class ChannelTest(unittest.TestCase):
    def test_supports_suggested_actions(self):
        actual = Channel.supports_suggested_actions(Channels.facebook, 5)
        self.assertTrue(actual)

    def test_supports_suggested_actions_many(self):
        supports_suggested_actions_data: List[Tuple[Channels, int, bool]] = [
            (Channels.line, 13, True),
            (Channels.line, 14, False),
            (Channels.skype, 10, True),
            (Channels.skype, 11, False),
            (Channels.kik, 20, True),
            (Channels.kik, 21, False),
            (Channels.emulator, 100, True),
            (Channels.emulator, 101, False),
        ]

        for channel, button_cnt, expected in supports_suggested_actions_data:
            with self.subTest(
                channel=channel, button_cnt=button_cnt, expected=expected
            ):
                actual = Channel.supports_suggested_actions(channel, button_cnt)
                self.assertEqual(expected, actual)

    def test_supports_card_actions_many(self):
        supports_card_action_data: List[Tuple[Channels, int, bool]] = [
            (Channels.line, 99, True),
            (Channels.line, 100, False),
            (Channels.slack, 100, True),
            (Channels.skype, 3, True),
            (Channels.skype, 5, False),
        ]

        for channel, button_cnt, expected in supports_card_action_data:
            with self.subTest(
                channel=channel, button_cnt=button_cnt, expected=expected
            ):
                actual = Channel.supports_card_actions(channel, button_cnt)
                self.assertEqual(expected, actual)

    def test_should_return_channel_id_from_context_activity(self):
        test_activity = Activity(channel_id=Channels.facebook)
        test_context = TurnContext(BotFrameworkAdapter(settings=None), test_activity)
        channel_id = Channel.get_channel_id(test_context)
        self.assertEqual(Channels.facebook, channel_id)

    def test_should_return_empty_from_context_activity_missing_channel(self):
        test_activity = Activity(channel_id=None)
        test_context = TurnContext(BotFrameworkAdapter(settings=None), test_activity)
        channel_id = Channel.get_channel_id(test_context)
        self.assertEqual("", channel_id)
