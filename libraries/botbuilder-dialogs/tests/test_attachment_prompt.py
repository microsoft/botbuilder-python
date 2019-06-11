# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.dialogs.prompts import AttachmentPrompt, PromptOptions, PromptRecognizerResult
from botbuilder.schema import Activity, InputHints

from botbuilder.core.turn_context import TurnContext
from botbuilder.core.adapters import TestAdapter

class AttachmentPromptTests(aiounittest.AsyncTestCase):
    def test_attachment_prompt_with_empty_id_should_fail(self):
        empty_id = ''

        with self.assertRaises(TypeError):
            AttachmentPrompt(empty_id)
    
    def test_attachment_prompt_with_none_id_should_fail(self):
        with self.assertRaises(TypeError):
            AttachmentPrompt(None)
    
    

