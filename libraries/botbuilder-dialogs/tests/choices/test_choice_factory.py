# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import unittest
from typing import List

from botbuilder.dialogs.choices import Choice, ChoiceFactory, ChoiceFactoryOptions
from botbuilder.schema import (
    ActionTypes,
    Activity,
    ActivityTypes,
    Attachment,
    AttachmentLayoutTypes,
    CardAction,
    HeroCard,
    InputHints,
    SuggestedActions,
)
from botframework.connector import Channels


class ChoiceFactoryTest(unittest.TestCase):
    color_choices: List[Choice] = [Choice("red"), Choice("green"), Choice("blue")]
    choices_with_actions: List[Choice] = [
        Choice(
            "ImBack",
            action=CardAction(
                type=ActionTypes.im_back, title="ImBack Action", value="ImBack Value"
            ),
        ),
        Choice(
            "MessageBack",
            action=CardAction(
                type=ActionTypes.message_back,
                title="MessageBack Action",
                value="MessageBack Value",
            ),
        ),
        Choice(
            "PostBack",
            action=CardAction(
                type=ActionTypes.post_back,
                title="PostBack Action",
                value="PostBack Value",
            ),
        ),
    ]

    def test_inline_should_render_choices_inline(self):
        activity = ChoiceFactory.inline(ChoiceFactoryTest.color_choices, "select from:")
        self.assertEqual("select from: (1) red, (2) green, or (3) blue", activity.text)

    def test_should_render_choices_as_a_list(self):
        activity = ChoiceFactory.list_style(
            ChoiceFactoryTest.color_choices, "select from:"
        )
        self.assertEqual(
            "select from:\n\n   1. red\n   2. green\n   3. blue", activity.text
        )

    def test_should_render_unincluded_numbers_choices_as_a_list(self):
        activity = ChoiceFactory.list_style(
            ChoiceFactoryTest.color_choices,
            "select from:",
            options=ChoiceFactoryOptions(include_numbers=False),
        )
        self.assertEqual(
            "select from:\n\n   - red\n   - green\n   - blue", activity.text
        )

    def test_should_render_choices_as_suggested_actions(self):
        expected = Activity(
            type=ActivityTypes.message,
            text="select from:",
            input_hint=InputHints.expecting_input,
            suggested_actions=SuggestedActions(
                actions=[
                    CardAction(type=ActionTypes.im_back, value="red", title="red"),
                    CardAction(type=ActionTypes.im_back, value="green", title="green"),
                    CardAction(type=ActionTypes.im_back, value="blue", title="blue"),
                ]
            ),
        )

        activity = ChoiceFactory.suggested_action(
            ChoiceFactoryTest.color_choices, "select from:"
        )

        self.assertEqual(expected, activity)

    def test_should_render_choices_as_hero_card(self):
        expected = Activity(
            type=ActivityTypes.message,
            input_hint=InputHints.expecting_input,
            attachment_layout=AttachmentLayoutTypes.list,
            attachments=[
                Attachment(
                    content=HeroCard(
                        text="select from:",
                        buttons=[
                            CardAction(
                                type=ActionTypes.im_back, value="red", title="red"
                            ),
                            CardAction(
                                type=ActionTypes.im_back, value="green", title="green"
                            ),
                            CardAction(
                                type=ActionTypes.im_back, value="blue", title="blue"
                            ),
                        ],
                    ),
                    content_type="application/vnd.microsoft.card.hero",
                )
            ],
        )

        activity = ChoiceFactory.hero_card(
            ChoiceFactoryTest.color_choices, "select from:"
        )

        self.assertEqual(expected, activity)

    def test_should_automatically_choose_render_style_based_on_channel_type(self):
        expected = Activity(
            type=ActivityTypes.message,
            text="select from:",
            input_hint=InputHints.expecting_input,
            suggested_actions=SuggestedActions(
                actions=[
                    CardAction(type=ActionTypes.im_back, value="red", title="red"),
                    CardAction(type=ActionTypes.im_back, value="green", title="green"),
                    CardAction(type=ActionTypes.im_back, value="blue", title="blue"),
                ]
            ),
        )
        activity = ChoiceFactory.for_channel(
            Channels.emulator, ChoiceFactoryTest.color_choices, "select from:"
        )

        self.assertEqual(expected, activity)

    def test_should_choose_correct_styles_for_teams(self):
        expected = Activity(
            type=ActivityTypes.message,
            input_hint=InputHints.expecting_input,
            attachment_layout=AttachmentLayoutTypes.list,
            attachments=[
                Attachment(
                    content=HeroCard(
                        text="select from:",
                        buttons=[
                            CardAction(
                                type=ActionTypes.im_back, value="red", title="red"
                            ),
                            CardAction(
                                type=ActionTypes.im_back, value="green", title="green"
                            ),
                            CardAction(
                                type=ActionTypes.im_back, value="blue", title="blue"
                            ),
                        ],
                    ),
                    content_type="application/vnd.microsoft.card.hero",
                )
            ],
        )
        activity = ChoiceFactory.for_channel(
            Channels.ms_teams, ChoiceFactoryTest.color_choices, "select from:"
        )
        self.assertEqual(expected, activity)

    def test_should_include_choice_actions_in_suggested_actions(self):
        expected = Activity(
            type=ActivityTypes.message,
            text="select from:",
            input_hint=InputHints.expecting_input,
            suggested_actions=SuggestedActions(
                actions=[
                    CardAction(
                        type=ActionTypes.im_back,
                        value="ImBack Value",
                        title="ImBack Action",
                    ),
                    CardAction(
                        type=ActionTypes.message_back,
                        value="MessageBack Value",
                        title="MessageBack Action",
                    ),
                    CardAction(
                        type=ActionTypes.post_back,
                        value="PostBack Value",
                        title="PostBack Action",
                    ),
                ]
            ),
        )
        activity = ChoiceFactory.suggested_action(
            ChoiceFactoryTest.choices_with_actions, "select from:"
        )
        self.assertEqual(expected, activity)

    def test_should_include_choice_actions_in_hero_cards(self):
        expected = Activity(
            type=ActivityTypes.message,
            input_hint=InputHints.expecting_input,
            attachment_layout=AttachmentLayoutTypes.list,
            attachments=[
                Attachment(
                    content=HeroCard(
                        text="select from:",
                        buttons=[
                            CardAction(
                                type=ActionTypes.im_back,
                                value="ImBack Value",
                                title="ImBack Action",
                            ),
                            CardAction(
                                type=ActionTypes.message_back,
                                value="MessageBack Value",
                                title="MessageBack Action",
                            ),
                            CardAction(
                                type=ActionTypes.post_back,
                                value="PostBack Value",
                                title="PostBack Action",
                            ),
                        ],
                    ),
                    content_type="application/vnd.microsoft.card.hero",
                )
            ],
        )
        activity = ChoiceFactory.hero_card(
            ChoiceFactoryTest.choices_with_actions, "select from:"
        )
        self.assertEqual(expected, activity)
