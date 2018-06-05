# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from botbuilder.core import CardFactory
from botbuilder.schema import (ActionTypes, AnimationCard, Attachment, AudioCard,
                               CardAction, CardImage, HeroCard, MediaUrl, OAuthCard,
                               SigninCard, ThumbnailCard, ReceiptCard, VideoCard)


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
    def test_should_create_adaptive_card_attachment(self):
        attachment = CardFactory.adaptive_card({'type': 'AdaptiveCard'})
        assert_attachment(attachment, CardFactory.content_types.adaptive_card)
        assert attachment.content['type'] is not None

    def test_should_raise_error_for_adaptive_card_if_card_is_not_dict(self):
        try:
            attachment = CardFactory.adaptive_card(None)
        except TypeError:
            pass
        else:
            assert False, 'should have raise TypeError'

    def test_should_create_animation_card_attachment(self):
        media = [MediaUrl(url='https://example.org/media')]
        card = AnimationCard(title='test', media=media)
        attachment = CardFactory.animation_card(card)

        assert_attachment(attachment, CardFactory.content_types.animation_card)
        assert attachment.content.title == 'test', 'wrong title'
        assert_media(attachment.content.media, 1, ['https://example.org/media'])

    def test_should_raise_error_for_animation_card_if_card_is_not_animation_card(self):
        try:
            attachment = CardFactory.animation_card(None)
        except TypeError:
            pass
        else:
            assert False, 'should have raise TypeError'

    def test_should_create_audio_card_attachment(self):
        media = [MediaUrl(url='https://example.org/media')]
        card = AudioCard(title='test', media=media)
        attachment = CardFactory.audio_card(card)

        assert_attachment(attachment, CardFactory.content_types.audio_card)
        assert attachment.content.title == 'test', 'wrong title.'
        assert_media(attachment.content.media, 1, ['https://example.org/media'])

    def test_should_raise_error_for_audio_card_if_card_is_not_audio_card(self):
        try:
            attachment = CardFactory.audio_card(None)
        except TypeError:
            pass
        else:
            assert False, 'should have raise TypeError'

    def test_should_create_video_card_attachment(self):
        media = [MediaUrl(url='https://example.org/media')]
        card = VideoCard(title='test', media=media)
        attachment = CardFactory.video_card(card)

        assert_attachment(attachment, CardFactory.content_types.video_card)
        assert attachment.content.title == 'test', 'wrong title.'
        assert_media(attachment.content.media, 1, ['https://example.org/media'])

    def test_should_raise_error_for_video_card_if_card_is_not_video_card(self):
        try:
            attachment = CardFactory.video_card(None)
        except TypeError:
            pass
        else:
            assert False, 'should have raise TypeError'

    def test_should_create_hero_card_attachment(self):
        card = HeroCard(title='test')
        attachment = CardFactory.hero_card(card)

        assert_attachment(attachment, CardFactory.content_types.hero_card)
        assert attachment.content.title == 'test', 'wrong title.'

    def test_should_raise_error_for_hero_card_if_card_is_not_hero_card(self):
        try:
            attachment = CardFactory.hero_card(None)
        except TypeError:
            pass
        else:
            assert False, 'should have raise TypeError'

    def test_should_create_thumbnail_card_attachment(self):
        card = ThumbnailCard(title='test')
        attachment = CardFactory.thumbnail_card(card)

        assert_attachment(attachment, CardFactory.content_types.thumbnail_card)
        assert attachment.content.title == 'test', 'wrong title.'

    def test_should_raise_error_for_thumbnail_card_if_card_is_not_thumbnail_card(self):
        try:
            attachment = CardFactory.thumbnail_card(None)
        except TypeError:
            pass
        else:
            assert False, 'should have raise TypeError'

    def test_should_create_receipt_card_attachment(self):
        card = ReceiptCard(title='test')
        attachment = CardFactory.receipt_card(card)

        assert_attachment(attachment, CardFactory.content_types.receipt_card)
        assert attachment.content.title == 'test', 'wrong title.'

    def test_should_raise_error_for_receipt_card_if_card_is_not_receipt_card(self):
        try:
            attachment = CardFactory.receipt_card(None)
        except TypeError:
            pass
        else:
            assert False, 'should have raise TypeError'

    def test_should_create_signin_card_attachment(self):
        button = CardAction(type=ActionTypes.signin, title='test', value='https://example.org/signin')
        card = SigninCard(title='test', buttons=[button])
        attachment = CardFactory.signin_card(card)

        assert_attachment(attachment, CardFactory.content_types.signin_card)
        assert_actions(attachment.content.buttons, 1, ['test'])
        assert attachment.content.buttons[0].type == 'signin', 'wrong action type.'
        assert attachment.content.buttons[0].value == 'https://example.org/signin', 'wrong action value.'

    def test_should_raise_error_for_signin_card_if_card_is_not_signin_card(self):
        try:
            attachment = CardFactory.signin_card(None)
        except TypeError:
            pass
        else:
            assert False, 'should have raise TypeError'

    def test_should_create_oauth_card_attachment(self):
        button = CardAction(type=ActionTypes.signin, title='test', value='https://example.org/signin')
        card = OAuthCard(text='sign in', connection_name='test.com', buttons=[button])
        attachment = CardFactory.oauth_card(card)

        assert_attachment(attachment, CardFactory.content_types.oauth_card)
        assert_actions(attachment.content.buttons, 1, ['test'])
        assert attachment.content.text == 'sign in', 'wrong text'
        assert attachment.content.connection_name == 'test.com', 'wrong connection_name'

    def test_should_raise_error_for_oauth_card_if_card_is_not_oauth_card(self):
        try:
            attachment = CardFactory.oauth_card(None)
        except TypeError:
            pass
        else:
            assert False, 'should have raise TypeError'
