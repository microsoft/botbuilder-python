# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import (
    AnimationCard,
    Attachment,
    AudioCard,
    HeroCard,
    OAuthCard,
    ReceiptCard,
    SigninCard,
    ThumbnailCard,
    VideoCard,
)


class ContentTypes:
    adaptive_card = "application/vnd.microsoft.card.adaptive"
    animation_card = "application/vnd.microsoft.card.animation"
    audio_card = "application/vnd.microsoft.card.audio"
    hero_card = "application/vnd.microsoft.card.hero"
    receipt_card = "application/vnd.microsoft.card.receipt"
    oauth_card = "application/vnd.microsoft.card.oauth"
    signin_card = "application/vnd.microsoft.card.signin"
    thumbnail_card = "application/vnd.microsoft.card.thumbnail"
    video_card = "application/vnd.microsoft.card.video"


class CardFactory:
    content_types = ContentTypes

    @staticmethod
    def adaptive_card(card: dict) -> Attachment:
        """
        Returns an attachment for an adaptive card. The attachment will contain the card and the
        appropriate 'contentType'. Will raise a TypeError if the 'card' argument is not an
        dict.
        :param card:
        :return:
        """
        if not isinstance(card, dict):
            raise TypeError(
                "CardFactory.adaptive_card(): `card` argument is not of type dict, unable to prepare "
                "attachment."
            )

        return Attachment(
            content_type=CardFactory.content_types.adaptive_card, content=card
        )

    @staticmethod
    def animation_card(card: AnimationCard) -> Attachment:
        """
        Returns an attachment for an animation card. Will raise a TypeError if the 'card' argument is not an
        AnimationCard.
        :param card:
        :return:
        """
        if not isinstance(card, AnimationCard):
            raise TypeError(
                "CardFactory.animation_card(): `card` argument is not an instance of an AnimationCard, "
                "unable to prepare attachment."
            )

        return Attachment(
            content_type=CardFactory.content_types.animation_card, content=card
        )

    @staticmethod
    def audio_card(card: AudioCard) -> Attachment:
        """
        Returns an attachment for an audio card. Will raise a TypeError if 'card' argument is not an AudioCard.
        :param card:
        :return:
        """
        if not isinstance(card, AudioCard):
            raise TypeError(
                "CardFactory.audio_card(): `card` argument is not an instance of an AudioCard, "
                "unable to prepare attachment."
            )

        return Attachment(
            content_type=CardFactory.content_types.audio_card, content=card
        )

    @staticmethod
    def hero_card(card: HeroCard) -> Attachment:
        """
        Returns an attachment for a hero card. Will raise a TypeError if 'card' argument is not a HeroCard.

        Hero cards tend to have one dominant full width image and the cards text & buttons can
        usually be found below the image.
        :return:
        """
        if not isinstance(card, HeroCard):
            raise TypeError(
                "CardFactory.hero_card(): `card` argument is not an instance of an HeroCard, "
                "unable to prepare attachment."
            )

        return Attachment(
            content_type=CardFactory.content_types.hero_card, content=card
        )

    @staticmethod
    def oauth_card(card: OAuthCard) -> Attachment:
        """
        Returns an attachment for an OAuth card used by the Bot Frameworks Single Sign On (SSO) service. Will raise a
        TypeError if 'card' argument is not a OAuthCard.
        :param card:
        :return:
        """
        if not isinstance(card, OAuthCard):
            raise TypeError(
                "CardFactory.oauth_card(): `card` argument is not an instance of an OAuthCard, "
                "unable to prepare attachment."
            )

        return Attachment(
            content_type=CardFactory.content_types.oauth_card, content=card
        )

    @staticmethod
    def receipt_card(card: ReceiptCard) -> Attachment:
        """
        Returns an attachment for a receipt card. Will raise a TypeError if 'card' argument is not a ReceiptCard.
        :param card:
        :return:
        """
        if not isinstance(card, ReceiptCard):
            raise TypeError(
                "CardFactory.receipt_card(): `card` argument is not an instance of an ReceiptCard, "
                "unable to prepare attachment."
            )

        return Attachment(
            content_type=CardFactory.content_types.receipt_card, content=card
        )

    @staticmethod
    def signin_card(card: SigninCard) -> Attachment:
        """
        Returns an attachment for a signin card. For channels that don't natively support signin cards an alternative
        message will be rendered. Will raise a TypeError if 'card' argument is not a SigninCard.
        :param card:
        :return:
        """
        if not isinstance(card, SigninCard):
            raise TypeError(
                "CardFactory.signin_card(): `card` argument is not an instance of an SigninCard, "
                "unable to prepare attachment."
            )

        return Attachment(
            content_type=CardFactory.content_types.signin_card, content=card
        )

    @staticmethod
    def thumbnail_card(card: ThumbnailCard) -> Attachment:
        """
        Returns an attachment for a thumbnail card. Thumbnail cards are similar to
        but instead of a full width image, they're typically rendered with a smaller thumbnail version of
        the image on either side and the text will be rendered in column next to the image. Any buttons
        will typically show up under the card. Will raise a TypeError if 'card' argument is not a ThumbnailCard.
        :param card:
        :return:
        """
        if not isinstance(card, ThumbnailCard):
            raise TypeError(
                "CardFactory.thumbnail_card(): `card` argument is not an instance of an ThumbnailCard, "
                "unable to prepare attachment."
            )

        return Attachment(
            content_type=CardFactory.content_types.thumbnail_card, content=card
        )

    @staticmethod
    def video_card(card: VideoCard) -> Attachment:
        """
        Returns an attachment for a video card. Will raise a TypeError if 'card' argument is not a VideoCard.
        :param card:
        :return:
        """
        if not isinstance(card, VideoCard):
            raise TypeError(
                "CardFactory.video_card(): `card` argument is not an instance of an VideoCard, "
                "unable to prepare attachment."
            )

        return Attachment(
            content_type=CardFactory.content_types.video_card, content=card
        )
