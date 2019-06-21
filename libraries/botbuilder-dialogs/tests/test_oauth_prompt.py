# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.dialogs.prompts import OAuthPromptSettings
from botbuilder.schema import Activity, InputHints

from botbuilder.core.turn_context import TurnContext
from botbuilder.core.adapters import TestAdapter

class OAuthPromptTests(aiounittest.AsyncTestCase):
    async def test_does_the_things(self):
      pass