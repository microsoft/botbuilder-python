# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import warnings
from typing import Any, List, Union
from botbuilder.schema import (ActionTypes, AnimationCard, Attachment, AudioCard,
                               CardAction, CardImage, Fact, HeroCard,
                               MediaUrl, OAuthCard, ReceiptCard,
                               ReceiptItem, SigninCard, ThumbnailCard, VideoCard)


class ContentTypes:
    adaptive_card = 'application/vnd.microsoft.card.adaptive'
    animation_card = 'application/vnd.microsoft.card.animation'
    audio_card = 'application/vnd.microsoft.card.audio'
    hero_card = 'application/vnd.microsoft.card.hero'
    receipt_card = 'application/vnd.microsoft.card.receipt'
    oauth_card = 'application/vnd.microsoft.card.oauth'
    signin_card = 'application/vnd.microsoft.card.signin'
    thumbnail_card = 'application/vnd.microsoft.card.thumbnail'
    video_card = 'application/vnd.microsoft.card.video'


class CardFactory:
    content_types = ContentTypes

    @staticmethod
    def adaptive_card(card: Any) -> Attachment:
        """
        Returns an attachment for an adaptive card. The attachment will contain the card and the
        appropriate 'contentType'.
        :param card:
        :return:
        """
        return Attachment(content_type=CardFactory.content_types.adaptive_card,
                          content=card)

    @staticmethod
    def animation_card(title: str, media: List[Union[MediaUrl, str]],
                       buttons: List[Union[CardAction, str]] = None, other: AnimationCard = None) -> Attachment:
        """
        Returns an attachment for an animation card. Will emit an error if the `other` parameter is not an
        AnimationCard.
        :param title:
        :param media:
        :param buttons:
        :param other:
        :return:
        """
        card = AnimationCard()
        if isinstance(other, AnimationCard):
            card = other
        elif other is not None:
            warnings.warn('CardFactory.animation_card(): `other` parameter is not an instance of an AnimationCard, '
                          'ignoring `other` in card generation.')
        if title:
            card.title = title
        if media:
            card.media = CardFactory.media(media)
        if buttons:
            card.buttons = CardFactory.actions(buttons)

        return Attachment(content_type=CardFactory.content_types.animation_card,
                          content=card)

    @staticmethod
    def audio_card(title: str, media: List[Union[str, MediaUrl]],
                   buttons: List[Union[str, CardAction]] = None, other: AudioCard = None) -> Attachment:
        card = AudioCard()
        if isinstance(other, AudioCard):
            card = other
        elif other is not None:
            warnings.warn('CardFactory.audio_card(): `other` parameter is not an instance of an AudioCard, ignoring '
                          '`other` in card generation.')
        if title:
            card.title = title
        if media:
            card.media = CardFactory.media(media)
        if buttons:
            card.buttons = CardFactory.actions(buttons)

        return Attachment(content_type=CardFactory.content_types.audio_card,
                          content=card)

    @staticmethod
    def hero_card(title: str, text: str = None, images: List[Union[str, CardImage]] = None,
                  buttons: List[Union[str, CardImage]] = None, other: HeroCard = None) -> Attachment:
        """
        Returns an attachment for a hero card.

        Hero cards tend to have one dominant full width image and the cards text & buttons can
        usually be found below the image.
        :return:
        """
        card = HeroCard()
        if isinstance(other, HeroCard):
            card = other
        elif other is not None:
            warnings.warn('CardFactory.hero_card(): `other` parameter is not an instance of an HeroCard, '
                          'ignoring `other` in card generation.')
        if title:
            card.title = title
        if text:
            card.text = text
        if images:
            card.images = CardFactory.images(images)
        if buttons:
            card.buttons = CardFactory.actions(buttons)

        return Attachment(content_type=CardFactory.content_types.hero_card,
                          content=card)

    @staticmethod
    def oauth_card(connection_name, title: str, text: str = None) -> Attachment:
        """
        Returns an attachment for an OAuth card used by the Bot Frameworks Single Sign On (SSO) service.
        :param connection_name:
        :param title:
        :param text:
        :return:
        """
        button = CardAction(type=ActionTypes.signin, title=title, value=None)
        card = OAuthCard(connection_name=connection_name, buttons=[button], text=text)

        return Attachment(content_type=CardFactory.content_types.oauth_card,
                          content=card)

    @staticmethod
    def receipt_card(title: str = None, facts: List[Fact] = None, items: List[ReceiptItem] = None,
                     tap: CardAction = None,
                     total: str = None, tax: str = None, vat: str = None,
                     buttons: List[CardAction] = None, other: ReceiptCard = None) -> Attachment:
        """
        Returns an attachment for a receipt card. The attachment will contain the parameters and the appropriate
        `contentType`.
        :param title:
        :param facts:
        :param items:
        :param tap:
        :param total:
        :param tax:
        :param vat:
        :param buttons:
        :param other:
        :return:
        """
        card = ReceiptCard()
        if isinstance(other, ReceiptCard):
            card = other
        elif other is not None:
            warnings.warn('CardFactory.receipt_card(): `other` parameter is not an instance of an ReceiptCard, '
                          'ignoring `other` in card generation.')

        if title is not None:
            card.title = title
        if facts is not None:
            card.facts = facts
        if items is not None:
            card.items = items
        if tap is not None:
            card.tap = tap
        if total is not None:
            card.total = total
        if tax is not None:
            card.tax = tax
        if vat is not None:
            card.vat = vat
        if buttons is not None:
            card.buttons = buttons

        return Attachment(content_type=CardFactory.content_types.receipt_card,
                          content=card)

    @staticmethod
    def signin_card(title: str, url: str, text: str = None) -> Attachment:
        """
        Returns an attachment for a signin card. For channels that don't natively support signin cards an alternative
        message will be rendered.
        :param title:
        :param url:
        :param text:
        :return:
        """
        button = CardAction(type=ActionTypes.signin, title=title, value=url)
        card = SigninCard(text=text, buttons=[button])

        return Attachment(content_type=CardFactory.content_types.signin_card,
                          content=card)

    @staticmethod
    def thumbnail_card(title: str, text: str = None, images: List[Union[str, CardImage]] = None,
                       buttons: List[Union[CardAction, str]] = None, other: ThumbnailCard = None) -> Attachment:
        """
        Returns an attachment for a thumbnail card. Thumbnail cards are similar to [hero cards](#herocard)
        but instead of a full width image, they're typically rendered with a smaller thumbnail version of
        the image on either side and the text will be rendered in column next to the image. Any buttons
        will typically show up under the card.
        :param title:
        :param text:
        :param images:
        :param buttons:
        :param other:
        :return:
        """
        card = ThumbnailCard()
        if isinstance(other, ThumbnailCard):
            card = other
        elif other is not None:
            warnings.warn('CardFactory.thumbnail_card(): `other` parameter is not an instance of an ThumbnailCard, '
                          'ignoring `other` in card generation.')
        if title:
            card.title = title
        if text:
            card.text = text
        if images:
            card.images = CardFactory.images(images)
        if buttons:
            card.buttons = CardFactory.actions(buttons)

        return Attachment(content_type=CardFactory.content_types.thumbnail_card,
                          content=card)

    @staticmethod
    def video_card(title: str, media: List[Union[str, MediaUrl]],
                   buttons: List[Union[CardAction, str]] = None, other: VideoCard = None) -> Attachment:
        """
        Returns an attachment for a video card.
        :param title:
        :param media:
        :param buttons:
        :param other:
        :return:
        """
        card = VideoCard()
        if isinstance(other, VideoCard):
            card = other
        elif other is not None:
            warnings.warn('CardFactory.video_card(): `other` parameter is not an instance of an VideoCard, '
                          'ignoring `other` in card generation.')
        if title:
            card.title = title
        if media:
            card.media = CardFactory.media(media)
        if buttons:
            card.buttons = CardFactory.actions(buttons)

        return Attachment(content_type=CardFactory.content_types.video_card,
                          content=card)

    @staticmethod
    def actions(actions: List[Union[CardAction, str]]) -> List[CardAction]:
        if actions is None:
            return []

        def prepare_action(action_or_str):
            if isinstance(action_or_str, CardAction):
                return action_or_str
            else:
                return CardAction(type=ActionTypes.im_back, value=str(action_or_str), title=str(action_or_str))

        return [prepare_action(action) for action in actions]

    @staticmethod
    def images(images: List[Union[CardImage, str]]) -> List[CardImage]:
        if images is None:
            return []

        def prepare_image(image_or_str):
            if isinstance(image_or_str, CardImage):
                return image_or_str
            else:
                return CardImage(url=image_or_str)

        return [prepare_image(image) for image in images]

    @staticmethod
    def media(links: List[Union[MediaUrl, str]]) -> List[MediaUrl]:
        if links is None:
            return []

        def prepare_media(media_or_str):
            if isinstance(media_or_str, MediaUrl):
                return media_or_str
            else:
                return MediaUrl(url=media_or_str)

        return [prepare_media(link) for link in links]
