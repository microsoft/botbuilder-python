# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import warnings

from typing import List
from botbuilder.core import CardFactory
from botbuilder.schema import (AnimationCard, Attachment, AudioCard,
                               CardAction, CardImage,
                               MediaUrl, ThumbnailCard, VideoCard)


def assert_attachment(attachment: Attachment, content_type: str):
    assert attachment is not None, 'attachment not created'
    assert attachment.content_type == content_type, 'attachment has wrong content_type'
    assert attachment.content is not None, 'attachment missing context'


def assert_actions(actions: List[CardAction], count: int, titles: List[str] = None):
    assert type(actions) == list, 'actions is not a list'
    assert len(actions) == count, 'wrong number of actions returned'
    for idx, action in enumerate(actions):
        # Added type checking
        assert isinstance(action, CardAction), f'action[{idx}] is not a CardAction object'

        assert action.title is not None, f'title[{idx}] missing'
        if titles is not None:
            assert action.title == titles[idx], f'title[{idx}] invalid'
        assert action.type is not None, f'type[{idx}] missing'
        assert action.value is not None, f'value[{idx}] missing'


def assert_images(images: List[CardImage], count: int, links: List[str] = None):
    assert type(images) == list, 'images is not a list'
    assert len(images) == count, 'wrong number of images returned'
    for idx, image in enumerate(images):
        # Added type checking
        assert isinstance(image, CardImage), f'image[{idx}] is not a CardImage object'

        assert image.url is not None, f'image url[{idx}] missing'
        if links is not None:
            assert image.url == links[idx], f'image url[{idx}] invalid'


def assert_media(media: List[MediaUrl], count: int, links: List[str] = None):
    assert type(media) == list, 'media is not a list'
    assert len(media) == count, 'wrong number of media returned'
    for idx, m in enumerate(media):
        # Added type checking
        assert isinstance(m, MediaUrl), f'media[{idx}] is not a MediaUrl object'

        assert m.url is not None, f'media url[{idx}] missing'
        if links is not None:
            assert m.url == links[idx], f'media url[{idx}] invalid'


class TestCardFactory:
    def test_should_convert_list_of_strings_passed_to_actions_to_card_actions(self):
        actions = CardFactory.actions(['a', 'b', 'c'])
        assert_actions(actions, 3, ['a', 'b', 'c'])

    def test_should_support_a_list_of_card_actions_options_passed_to_actions(self):
        actions = CardFactory.actions([CardAction(title='foo', type='postBack', value='test')])
        assert_actions(actions, 1, ['foo'])
        assert actions[0].type == 'postBack', 'incorrect action type'
        assert actions[0].value == 'test', 'incorrect action value'

    def test_should_support_a_none_type_actions_parameter_passed_to_actions(self):
        actions = CardFactory.actions(None)
        assert_actions(actions, 0)

    def test_should_map_array_of_strings_passed_to_images_to_card_image(self):
        images = CardFactory.images(['a', 'b', 'c'])
        assert_images(images, 3, ['a', 'b', 'c'])

    def test_should_support_a_list_of_card_image_options_passed_to_images(self):
        images = CardFactory.images([CardImage(url='foo', alt='test', tap=CardAction())])
        assert_images(images, 1, ['foo'])
        assert images[0].alt == 'test', 'incorrect image.alt property'
        assert isinstance(images[0].tap, CardAction), 'incorrect image.tap property'

    def test_should_support_a_none_type_actions_parameter_passed_to_images(self):
        actions = CardFactory.images(None)
        assert_actions(actions, 0)

    def test_should_map_list_of_strings_to_media_to_media_url_objects(self):
        media = CardFactory.media(['a', 'b', 'c'])
        assert_media(media, 3, ['a', 'b', 'c'])

    def test_should_support_list_of_media_url_objects_passed_to_media(self):
        media = CardFactory.media([MediaUrl(url='foo', profile='test')])
        assert_media(media, 1, ['foo'])
        assert media[0].profile == 'test', 'incorrect media.profile property'

    def test_should_support_none_type_media_parameter_passed_to_media(self):
        media = CardFactory.media(None)
        assert_media(media, 0)

    def test_should_create_adaptive_card(self):
        card = CardFactory.adaptive_card({'type': 'AdaptiveCard'})
        assert_attachment(card, CardFactory.content_types.adaptive_card)
        assert card.content['type'] is not None

    def test_should_create_animation_card(self):
        links = ['https://example.org/media']
        attachment = CardFactory.animation_card('foo', links)
        assert_attachment(attachment, CardFactory.content_types.animation_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title'
        assert_media(content.media, 1, links)

    def test_should_create_animation_card_with_buttons(self):
        links = ['https://example.org/media']
        attachment = CardFactory.animation_card('foo', links, ['a', 'b', 'c'])
        assert_attachment(attachment, CardFactory.content_types.animation_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title'
        assert_media(content.media, 1, links)
        assert_actions(content.buttons, 3, ['a', 'b', 'c'])

    def test_should_create_animation_card_with_other_fields(self):
        original_card = AnimationCard(text='test')
        links = ['https://example.org/media']

        attachment = CardFactory.animation_card('foo', links, other=original_card)
        assert_attachment(attachment, CardFactory.content_types.animation_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'
        assert content.text == 'test', 'missing or invalid other fields.'
        assert_media(content.media, 1, links)

    def test_should_create_animation_card_with_no_title(self):
        links = ['https://example.org/media']
        attachment = CardFactory.animation_card(None, links)
        assert_attachment(attachment, CardFactory.content_types.animation_card)
        content = attachment.content
        assert content.title is None, 'wrong title.'
        assert_media(content.media, 1, links)

    def test_should_create_audio_card(self):
        links = ['https://example.org/media']
        attachment = CardFactory.audio_card('foo', links)
        assert_attachment(attachment, CardFactory.content_types.audio_card)
        assert_attachment(attachment, CardFactory.content_types.audio_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'
        assert_media(content.media, 1, links)

    def test_should_create_audio_card_with_buttons(self):
        links = ['https://example.org/media']
        attachment = CardFactory.audio_card('foo', links, ['a', 'b', 'c'])
        assert_attachment(attachment, CardFactory.content_types.audio_card)
        assert_attachment(attachment, CardFactory.content_types.audio_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'
        assert_media(content.media, 1, links)
        assert_actions(content.buttons, 3, ['a', 'b', 'c'])

    def test_should_create_audio_card_with_other_fields(self):
        original_card = AudioCard(text='test')
        links = ['https://example.org/media']
        attachment = CardFactory.audio_card('foo', links, other=original_card)
        assert_attachment(attachment, CardFactory.content_types.audio_card)
        assert_attachment(attachment, CardFactory.content_types.audio_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'
        assert content.text == 'test', 'missing or invalid other fields.'
        assert_media(content.media, 1, links)

    def test_should_create_video_card(self):
        links = ['https://example.org/media']
        attachment = CardFactory.video_card('foo', links)
        assert_attachment(attachment, CardFactory.content_types.video_card)
        assert_attachment(attachment, CardFactory.content_types.video_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'
        assert_media(content.media, 1, links)

    def test_should_create_video_card_with_buttons(self):
        links = ['https://example.org/media']
        attachment = CardFactory.video_card('foo', links, ['a', 'b', 'c'])
        assert_attachment(attachment, CardFactory.content_types.video_card)
        assert_attachment(attachment, CardFactory.content_types.video_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'
        assert_media(content.media, 1, links)
        assert_actions(content.buttons, 3, ['a', 'b', 'c'])

    def test_should_create_video_card_with_other_fields(self):
        original_card = VideoCard(text='test')
        links = ['https://example.org/media']
        attachment = CardFactory.video_card('foo', links, other=original_card)
        assert_attachment(attachment, CardFactory.content_types.video_card)
        assert_attachment(attachment, CardFactory.content_types.video_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'
        assert content.text == 'test', 'missing or invalid other fields.'
        assert_media(content.media, 1, links)

    def test_should_create_hero_card(self):
        attachment = CardFactory.hero_card('foo')
        assert_attachment(attachment, CardFactory.content_types.hero_card)
        assert_attachment(attachment, CardFactory.content_types.hero_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'

    def test_should_create_thumbnail_card(self):
        attachment = CardFactory.thumbnail_card('foo')
        assert_attachment(attachment, CardFactory.content_types.thumbnail_card)
        assert_attachment(attachment, CardFactory.content_types.thumbnail_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'

    def test_should_create_thumbnail_card_with_images(self):
        links = ['https://example.org/image']
        attachment = CardFactory.thumbnail_card('foo', images=links)
        assert_attachment(attachment, CardFactory.content_types.thumbnail_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'
        assert_images(content.images, 1, links)

    def test_should_create_thumbnail_card_with_text(self):
        attachment = CardFactory.thumbnail_card('foo', 'test')
        assert_attachment(attachment, CardFactory.content_types.thumbnail_card)
        assert_attachment(attachment, CardFactory.content_types.thumbnail_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'
        assert content.text == 'test', 'wrong text.'

    def test_should_create_thumbnail_card_with_text_and_images(self):
        links = ['https://example.org/image']
        attachment = CardFactory.thumbnail_card('foo', 'test', links)
        assert_attachment(attachment, CardFactory.content_types.thumbnail_card)
        assert_attachment(attachment, CardFactory.content_types.thumbnail_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'
        assert content.text == 'test', 'wrong text.'
        assert_images(content.images, 1, links)

    def test_should_create_thumbnail_card_with_buttons(self):
        attachment = CardFactory.thumbnail_card('foo', buttons=['a', 'b', 'c'])
        assert_attachment(attachment, CardFactory.content_types.thumbnail_card)
        assert_attachment(attachment, CardFactory.content_types.thumbnail_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'
        assert_actions(content.buttons, 3, ['a', 'b', 'c'])

    def test_should_create_thumbnail_card_with_buttons_and_no_title(self):
        attachment = CardFactory.thumbnail_card(None, buttons=['a', 'b', 'c'])
        assert_attachment(attachment, CardFactory.content_types.thumbnail_card)
        assert_attachment(attachment, CardFactory.content_types.thumbnail_card)
        content = attachment.content
        assert content.title is None, 'wrong title.'
        assert_actions(content.buttons, 3, ['a', 'b', 'c'])

    def test_should_create_thumbnail_card_with_text_and_buttons(self):
        attachment = CardFactory.thumbnail_card('foo', 'test', None, ['a', 'b', 'c'])
        assert_attachment(attachment, CardFactory.content_types.thumbnail_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'
        assert content.text == 'test', 'wrong text.'
        assert_actions(content.buttons, 3, ['a', 'b', 'c'])

    def test_should_create_thumbnail_card_with_other(self):
        original_card = ThumbnailCard(subtitle='sub')
        attachment = CardFactory.thumbnail_card('foo', other=original_card)
        assert_attachment(attachment, CardFactory.content_types.thumbnail_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'
        assert content.subtitle == 'sub', 'wrong subtitle.'

    def test_should_create_thumbnail_card_with_text_and_other(self):
        original_card = ThumbnailCard(subtitle='sub')
        attachment = CardFactory.thumbnail_card('foo', 'test', None, None, other=original_card)
        assert_attachment(attachment, CardFactory.content_types.thumbnail_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong title.'
        assert content.text == 'test', 'wrong text.'
        assert content.subtitle == 'sub', 'wrong subtitle.'

    def test_should_create_receipt_card(self):
        attachment = CardFactory.receipt_card(title='foo')
        assert_attachment(attachment, CardFactory.content_types.receipt_card)
        content = attachment.content
        assert content.title == 'foo', 'wrong content.'

    def test_should_create_signin_card(self):
        attachment = CardFactory.signin_card('foo', 'https://example.org/signin')
        assert_attachment(attachment, CardFactory.content_types.signin_card)
        content = attachment.content
        assert_actions(content.buttons, 1, ['foo'])
        assert content.buttons[0].type == 'signin', 'wrong action type.'
        assert content.buttons[0].value == 'https://example.org/signin', 'wrong action value.'

    def test_should_create_signin_card_with_text(self):
        attachment = CardFactory.signin_card('foo', 'https://example.org/signin', 'test')
        assert_attachment(attachment, CardFactory.content_types.signin_card)
        content = attachment.content
        assert_actions(content.buttons, 1, ['foo'])
        assert content.buttons[0].type == 'signin', 'wrong action type.'
        assert content.buttons[0].value == 'https://example.org/signin', 'wrong action value.'
        assert content.text == 'test', 'wrong text.'

        """
        The below tests are examining if warnings are thrown when invalid Cards (the parameter `other` are passed into
        the CardFactory. The CardFactory will ignore `other` if the parameter does not match the type of content that is 
        returned with the final Attachment. The static methods themselves should still return Attachments with valid
        cards based off of the other provided parameters.
        """

    def test_animation_card_should_throw_warning_if_other_is_not_instance_of_animation_card(self):
        with warnings.catch_warnings(record=True) as w:
            CardFactory.animation_card('test', ['https://test.foo'], other='test')

            assert len(w) == 1

    def test_animation_card_should_not_throw_warning_if_other_is_instance_of_animation_card(self):
        with warnings.catch_warnings(record=True) as w:
            original_card = AnimationCard()
            CardFactory.animation_card('test', ['https://test.foo'], other=original_card)

            assert len(w) == 0

    def test_thumbnail_card_should_throw_warning_if_other_is_not_instance_of_thumbnail_card(self):
        with warnings.catch_warnings(record=True) as w:
            not_correct_card = AnimationCard()
            CardFactory.thumbnail_card('test', other=not_correct_card)

            assert len(w) == 1

    def test_thumbnail_card_should_not_throw_warning_if_other_is__instance_of_thumbnail_card(self):
        with warnings.catch_warnings(record=True) as w:
            original_card = ThumbnailCard()
            CardFactory.thumbnail_card('test', other=original_card)

            assert len(w) == 0
