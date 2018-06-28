# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import Choice, ChoiceFactory
from botbuilder.schema import Activity, InputHints, ActionTypes, CardAction, SuggestedActions


def assert_activity(received: Activity, expected: Activity):
    assert received.input_hint == expected.input_hint, f"Returned input_hint is invalid, [{received.input_hint}] != " \
                                                       f"[{expected.input_hint}]"
    if expected.text:
        assert received.text == expected.text
    if expected.suggested_actions:
        assert received.suggested_actions.actions is not None, 'suggested_Actions.actions not found.'
        assert len(received.suggested_actions.actions) == \
            len(expected.suggested_actions.actions), f"Invalid amount of actions returned " \
                                                     f"[{len(received.suggested_actions.actions)}] != " \
                                                     f"[{len(expected.suggested_actions.actions)}]"
        for index, e_action in enumerate(expected.suggested_actions.actions):
            r_action = received.suggested_actions.actions[index]
            assert e_action.type == r_action.type, f"Invalid type for action [{index}]"
            assert e_action.value == r_action.value, f"Invalid value for action [{index}]"
            assert e_action.title == r_action.title, f"Invalid title for action [{index}]"


COLOR_CHOICES = [Choice(value='red'), Choice(value='green'), Choice(value='blue')]


EXPECTED_ACTIONS = SuggestedActions(actions=[
    CardAction(type=ActionTypes.im_back,
               value='red',
               title='red'),
    CardAction(type=ActionTypes.im_back,
               value='green',
               title='green'),
    CardAction(type=ActionTypes.im_back,
               value='blue',
               title='blue')
])


class TestChoiceFactory:
    def test_should_render_choices_inline(self):
        activity = ChoiceFactory.inline(COLOR_CHOICES, 'select from:')
        assert_activity(activity, Activity(text='select from: (1) red, (2) green, or (3) blue',
                                           input_hint=InputHints.expecting_input))

    def test_should_render_choices_as_a_list(self):
        activity = ChoiceFactory.list(COLOR_CHOICES, 'select from:')
        assert_activity(activity, Activity(text='select from:\n\n   1. red\n   2. green\n   3. blue',
                                           input_hint=InputHints.expecting_input))

    def test_should_render_choices_as_suggested_actions(self):
        activity = ChoiceFactory.suggested_action(COLOR_CHOICES, 'select from:')
        assert_activity(activity, Activity(text='select from:',
                                           input_hint=InputHints.expecting_input,
                                           suggested_actions=EXPECTED_ACTIONS))

    def test_should_automatically_choose_render_style_based_on_channel_type(self):
        activity = ChoiceFactory.for_channel('emulator', COLOR_CHOICES, 'select from:')
        assert_activity(activity, Activity(text='select from:',
                                           input_hint=InputHints.expecting_input,
                                           suggested_actions=EXPECTED_ACTIONS))
