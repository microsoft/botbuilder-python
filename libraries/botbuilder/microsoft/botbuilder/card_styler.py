# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


from enum import Enum
from copy import deepcopy


class ContentTypes(Enum):
    """List of content types for each card style."""
    adaptive_card = 'application/vnd.microsoft.card.adaptive'
    animation_card = 'application/vnd.microsoft.card.animation'
    audio_card = 'application/vnd.microsoft.card.audio'
    hero_card = 'application/vnd.microsoft.card.hero'
    receipt_card = 'application/vnd.microsoft.card.receipt'
    signin_card = 'application/vnd.microsoft.card.signin'
    thumbnail_card = 'application/vnd.microsoft.card.thumbnail'
    video_card = 'application/vnd.microsoft.card.video'


class CardStyler(object):
    """
    A set of utility functions designed to assist with the formatting of the various card types a
    bot can return. All of these functions return an `Attachment` which can be added to an `Activity`
    directly or passed as input to a `MessageStyler` function.
    """
    content_types = ContentTypes
    """List of content types for each card style."""

    @staticmethod
    def adaptive_card(card):
        """
        Returns an attachment for an adaptive card. The attachment will contain the card and the
        appropriate `contentType`.

        Adaptive Cards are a new way for bots to send interactive and immersive card content to
        users. For channels that don't yet support Adaptive Cards natively, the Bot Framework will
        down render the card to an image that's been styled to look good on the target channel. For
        channels that support [hero cards](#herocards) you can continue to include Adaptive Card
        actions and they will be sent as buttons along with the rendered version of the card.

        For more information about Adaptive Cards and to download the latest SDK, visit
        [adaptivecards.io](http://adaptivecards.io/).
        :param card:
        :return:
        """
        return {
            'contentType': CardStyler.content_types.adaptive_card,
            'content': card
        }

    @staticmethod
    def animation_card(title, media, buttons=None, other=None):
        """
        Returns an attachment for an animation card.
        :param title:
        :param media:
        :param buttons:
        :param other:
        :return:
        """
        return media_card(CardStyler.content_types.animation_card, title, media, buttons, other)

    @staticmethod
    def audio_card(title, media, buttons=None, other=None):
        """
        Returns an attachment for an audio card.
        :param title:
        :param media:
        :param buttons:
        :param other:
        :return:
        """
        return media_card(CardStyler.content_types.audio_card, title, media, buttons, other)

    @staticmethod
    def hero_card(title, text=None, images=None, buttons=None, other=None):
        """
        Returns an attachment for a hero card. Hero cards tend to have one dominant full width image
        and the cards text & buttons can usually be found below the image.
        :param title:
        :param text:
        :param images:
        :param buttons:
        :param other:
        :return:
        """
        hero_card = CardStyler.thumbnail_card(title, text=text, images=images, buttons=buttons, other=other)
        hero_card['contentType'] = CardStyler.content_types.hero_card

    @staticmethod
    def receipt_card(card):
        """
        Returns an attachment for a receipt card. The attachment will contain the card and the
        appropriate `contentType`.
        :param card:
        :return:
        """
        return {'contentType': CardStyler.content_types.receipt_card, 'content': card}

    @staticmethod
    def signin_card(title, url, text=None):
        """
        Returns an attachment for a signin card. For channels that don't natively support signin
        cards an alternative message will be rendered.
        :param title:
        :param url:
        :param text:
        :return:
        """
        card = {'buttons': [{'type': 'signin', 'title': title, 'value': url}]}
        if text:
            card['text'] = text
        return {'contentType': CardStyler.content_types.signin_card, 'content': card}

    @staticmethod
    def thumbnail_card(title, text=None, images=None, buttons=None, other=None):
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
        if not isinstance(text, str):
            other = buttons
            buttons = images
            images = text
            text = None
        card = deepcopy(other)
        if title:
            card['title'] = title
        if text:
            card['text'] = text
        if images:
            card['images'] = CardStyler.images(images)
        if buttons:
            card['buttons'] = CardStyler.actions(buttons)

        return {'contentType': CardStyler.content_types.thumbnail_card, 'content': card}

    @staticmethod
    def video_card(title, media, buttons=None, other=None):
        """
        Returns an attachment for a video card.
        :param title:
        :param media:
        :param buttons:
        :param other:
        :return:
        """
        return media_card(CardStyler.content_types.video_card, title, media, buttons, other)

    @staticmethod
    def actions(*actions):
        """
        Returns a properly formatted array of actions. Supports converting strings to `messageBack`
        actions (note: using 'imBack' for now as 'messageBack' doesn't work properly in emulator.)
        :param actions:
        :return:
        """
        list_of_actions = []
        for action in actions:
            if isinstance(action, dict):  # what else might an action be?
                list_of_actions.append(action)
            else:
                list_of_actions.append({'type': 'imBack', 'value': str(action), 'title': str(action)})
        return list_of_actions

    @staticmethod
    def images(*images):
        """
        Returns a properly formatted array of card images.
        :param images:
        :return:
        """
        list_of_images = []
        for image in images:
            if isinstance(image, dict):
                list_of_images.append(image)
            else:
                list_of_images.append({'url': image})
        return list_of_images

    @staticmethod
    def media(*links):
        """
        Returns a properly formatted array of media url objects.
        :param links:
        :return:
        """
        list = []
        for link in links:
            if isinstance(links, dict):
                raise NotImplementedError()


def media_card(content_type, title, media, buttons=None, other=None):
    card = other or {}
    if title:
        card['title'] = title
    if media:
        card['media'] = CardStyler.media(media)
    if buttons:
        card['buttons'] = CardStyler.actions(buttons)
    return {'contentType': content_type, 'content': card}