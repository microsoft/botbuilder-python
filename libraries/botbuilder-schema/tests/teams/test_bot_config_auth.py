# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.schema.teams import BotConfigAuth


class TestBotConfigAuth(aiounittest.AsyncTestCase):
    def test_bot_config_auth_inits_with_no_args(self):
        bot_config_auth_response = BotConfigAuth()

        self.assertIsNotNone(bot_config_auth_response)
        self.assertIsInstance(bot_config_auth_response, BotConfigAuth)
        self.assertEqual("auth", bot_config_auth_response.type)
