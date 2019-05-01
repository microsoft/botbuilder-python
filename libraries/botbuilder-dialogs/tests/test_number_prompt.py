# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import aiounittest
from botbuilder.dialogs.prompts import NumberPrompt

class NumberPromptTests(aiounittest.AsyncTestCase):
    def test_empty_should_fail(self):
        empty_id = ''
        self.assertRaises(TypeError, lambda:NumberPrompt(empty_id))
    
