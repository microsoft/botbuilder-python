# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from botbuilder.core import MessageFactory
from botbuilder.schema import ActionTypes, Activity, Attachment, CardAction, InputHints, AttachmentLayoutTypes


def assert_message(activity: Activity):
    assert isinstance(activity, Activity), 'invalid activity returned'
    assert activity.type == 'message', 'not a message activity'


def assert_actions(actions: List[CardAction], count: int, titles: List[str] = None):
    assert type(actions) == list, 'actions not list'
    assert len(actions) == count, 'wrong number of actions returned'
    for idx, action in enumerate(actions):
        # Added type checking
        assert isinstance(action, CardAction), f'actions[{idx}] is not a CardAction'
        assert action.title is not None, f'title[{idx}] is missing'
        if titles is not None:
            assert action.title == titles[idx], f'title[{idx}] is incorrect'
        assert action.type is not None, f'type[{idx}] missing'
        assert action.value is not None, f'value[{idx}] missing'


def assert_attachments(activity: Activity, count: int, types: List[str] = None):
    assert type(activity.attachments) == list, 'no attachments array'
    assert len(activity.attachments) == count, 'wrong number of attachments'

    if types:
        for idx, attachment in enumerate(activity.attachments):
            # Added type checking
            assert isinstance(attachment, Attachment), f'attachment[{idx}] is not an Attachment'
            assert attachment.content_type == types[idx], f'attachment[{idx}] has invalid content_type'


class TestMessageFactory:

    suggested_actions = [CardAction(title='a', type=ActionTypes.im_back, value='a'),
                         CardAction(title='b', type=ActionTypes.im_back, value='b'),
                         CardAction(title='c', type=ActionTypes.im_back, value='c')]

    def test_should_return_a_simple_text_activity(self):
        activity = MessageFactory.text('test')
        assert_message(activity)
        assert activity.text == 'test', 'invalid text field'

    def test_should_return_a_simple_text_activity_with_text_and_speak(self):
        activity = MessageFactory.text('test', 'test2')
        assert_message(activity)
        assert activity.text == 'test', 'invalid text field'
        assert activity.speak == 'test2', 'invalid speak field'

    def test_should_return_a_simple_text_activity_with_text_speak_and_input_hint(self):
        activity = MessageFactory.text('test', 'test2', InputHints.ignoring_input)
        assert_message(activity)
        assert activity.text == 'test', 'invalid text field'
        assert activity.speak == 'test2', 'invalid speak field'
        assert activity.input_hint == InputHints.ignoring_input, 'invalid input_hint field'

    def test_should_return_suggested_actions(self):
        activity = MessageFactory.suggested_actions(self.suggested_actions)
        assert_message(activity)
        assert activity.suggested_actions is not None and \
            activity.suggested_actions.actions is not None, 'actions not returned'
        assert_actions(activity.suggested_actions.actions, 3, ['a', 'b', 'c'])

    def test_should_return_suggested_actions_with_text(self):
        activity = MessageFactory.suggested_actions(self.suggested_actions, 'test1')
        assert_message(activity)
        assert activity.suggested_actions is not None and \
            activity.suggested_actions.actions is not None, 'actions not returned'
        assert_actions(activity.suggested_actions.actions, 3, ['a', 'b', 'c'])
        assert activity.text == 'test1', 'invalid text field.'

    def test_should_return_suggested_actions_with_text_and_speak(self):
        activity = MessageFactory.suggested_actions(self.suggested_actions, 'test1', 'test2')
        assert_message(activity)
        assert activity.suggested_actions is not None and \
            activity.suggested_actions.actions is not None, 'actions not returned'
        assert_actions(activity.suggested_actions.actions, 3, ['a', 'b', 'c'])
        assert activity.text == 'test1', 'invalid text field.'
        assert activity.speak == 'test2', 'invalid speak field.'

    def test_should_return_suggested_actions_with_text_speak_and_input_hint(self):
        activity = MessageFactory.suggested_actions(self.suggested_actions, 'test1', 'test2', InputHints.ignoring_input)
        assert_message(activity)
        assert activity.suggested_actions is not None and \
            activity.suggested_actions.actions is not None, 'actions not returned'
        assert_actions(activity.suggested_actions.actions, 3, ['a', 'b', 'c'])
        assert activity.text == 'test1', 'invalid text field.'
        assert activity.speak == 'test2', 'invalid speak field.'
        assert activity.input_hint == InputHints.ignoring_input, 'invalid input_hint field.'

    def test_should_return_attachment(self):
        activity = MessageFactory.attachment(Attachment(content_type='none'))
        assert_message(activity)
        assert_attachments(activity, 1, ['none'])

    def test_should_return_attachment_with_text(self):
        activity = MessageFactory.attachment(Attachment(content_type='a'), 'test1')
        assert_message(activity)
        assert_attachments(activity, 1, ['a'])
        assert activity.text == 'test1', 'invalid text field.'

    def test_should_return_attachment_with_text_and_speak(self):
        activity = MessageFactory.attachment(Attachment(content_type='none'), 'test1', 'test2')
        assert_message(activity)
        assert_attachments(activity, 1, ['none'])
        assert activity.text == 'test1', 'invalid text field.'
        assert activity.speak == 'test2', 'invalid speak field.'

    def test_should_return_attachment_with_text_speak_and_input_hint(self):
        activity = MessageFactory.attachment(Attachment(content_type='none'),
                                             'test1', 'test2',
                                             InputHints.ignoring_input)
        assert_message(activity)
        assert_attachments(activity, 1, ['none'])
        assert activity.text == 'test1', 'invalid text field.'
        assert activity.speak == 'test2', 'invalid speak field.'
        assert activity.input_hint == InputHints.ignoring_input, 'invalid input_hint field.'

    def test_should_return_a_list(self):
        activity = MessageFactory.list([
            Attachment(content_type='a'),
            Attachment(content_type='b')
        ])
        assert_message(activity)
        assert_attachments(activity, 2, ['a', 'b'])
        assert activity.attachment_layout == AttachmentLayoutTypes.list, 'invalid attachment_layout.'

    def test_should_return_list_with_text_speak_and_input_hint(self):
        activity = MessageFactory.list([
            Attachment(content_type='a'),
            Attachment(content_type='b')
        ], 'test1', 'test2', InputHints.ignoring_input)
        assert_message(activity)
        assert_attachments(activity, 2, ['a', 'b'])
        assert activity.attachment_layout == AttachmentLayoutTypes.list, 'invalid attachment_layout.'
        assert activity.text == 'test1', 'invalid text field.'
        assert activity.speak == 'test2', 'invalid speak field.'
        assert activity.input_hint == InputHints.ignoring_input, 'invalid input_hint field.'

    def test_should_return_a_carousel(self):
        activity = MessageFactory.carousel([
            Attachment(content_type='a'),
            Attachment(content_type='b')
        ])
        assert_message(activity)
        assert_attachments(activity, 2, ['a', 'b'])
        assert activity.attachment_layout == AttachmentLayoutTypes.carousel, 'invalid attachment_layout.'

    def test_should_return_a_carousel_with_text_speak_and_input_hint(self):
        activity = MessageFactory.carousel([
            Attachment(content_type='a'),
            Attachment(content_type='b')
        ], 'test1', 'test2', InputHints.ignoring_input)
        assert_message(activity)
        assert_attachments(activity, 2, ['a', 'b'])
        assert activity.attachment_layout == AttachmentLayoutTypes.carousel, 'invalid attachment_layout.'
        assert activity.text == 'test1', 'invalid text field.'
        assert activity.speak == 'test2', 'invalid speak field.'
        assert activity.input_hint == InputHints.ignoring_input, 'invalid input_hint field.'

    def test_should_return_a_content_url(self):
        activity = MessageFactory.content_url('https://example.com/content', 'content-type')
        assert_message(activity)
        assert_attachments(activity, 1, ['content-type'])
        assert activity.attachments[0].content_url == 'https://example.com/content', \
            'invalid attachment[0].content_url.'

    def test_should_return_a_content_url_with_a_name(self):
        activity = MessageFactory.content_url('https://example.com/content', 'content-type', 'file name')
        assert_message(activity)
        assert_attachments(activity, 1, ['content-type'])
        assert activity.attachments[0].content_url == 'https://example.com/content', \
            'invalid attachment[0].content_url.'
        assert activity.attachments[0].name == 'file name', 'invalid attachment[0].name.'

    def test_should_return_a_content_url_with_a_name_text_speak_and_input_hint(self):
        activity = MessageFactory.content_url('https://example.com/content', 'content-type',
                                              'file name', 'test1',
                                              'test2', InputHints.ignoring_input)
        assert_message(activity)
        assert_attachments(activity, 1, ['content-type'])
        assert activity.attachments[0].content_url == 'https://example.com/content', \
            'invalid attachment[0].content_url.'
        assert activity.attachments[0].name == 'file name', 'invalid attachment[0].name.'
        assert activity.text == 'test1', 'invalid text field.'
        assert activity.speak == 'test2', 'invalid speak field.'
        assert activity.input_hint == InputHints.ignoring_input, 'invalid input_hint field.'
