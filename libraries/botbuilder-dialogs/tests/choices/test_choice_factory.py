# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import unittest
from typing import List

from botbuilder.core import CardFactory, MessageFactory
from botbuilder.dialogs.choices import (
    ChoiceFactory,
    Choice,
    ChoiceFactoryOptions
)
from botbuilder.schema import ActionTypes, Activity, CardAction, HeroCard, InputHints


class ChoiceFactoryTest(unittest.TestCase):
    color_choices = [Choice("red"), Choice("green"), Choice("blue")]

    def test_inline_should_render_choices_inline(self):
        activity = ChoiceFactory.inline(ChoiceFactoryTest.color_choices, "select from:")
        self.assertEqual("select from: (1) red, (2) green, or (3) blue", activity.text)
