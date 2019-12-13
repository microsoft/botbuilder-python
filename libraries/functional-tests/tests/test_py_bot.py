# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from unittest import TestCase

from direct_line_client import DirectLineClient


class PyBotTest(TestCase):
    def test_deployed_bot_answer(self):
        direct_line_secret = os.environ.get("DIRECT_LINE_KEY", "")
        if direct_line_secret == "":
            return

        client = DirectLineClient(direct_line_secret)
        user_message: str = "Contoso"

        send_result = client.send_message(user_message)
        self.assertIsNotNone(send_result)
        self.assertEqual(200, send_result.status_code)

        response, text = client.get_message()
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        self.assertEqual(f"You said '{user_message}'", text)
