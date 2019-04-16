# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import unittest

from botbuilder.dialogs.choices import Channel
from botframework.connector import Channels


class ChannelTest(unittest.TestCase):
    def test_supports_suggested_actions(self):
        actual = Channel.supports_suggested_actions(Channels.Facebook, 5)
        self.assertTrue(actual)
