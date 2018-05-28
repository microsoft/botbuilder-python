# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List, Union
from botbuilder.schema import (ActivityTypes, Activity, Attachment,
                               AttachmentLayoutTypes, CardAction, SuggestedActions, InputHints)

from .card_factory import CardFactory


def attachment_activity(attachment_layout: AttachmentLayoutTypes, attachments: List[Attachment], text: str = None,
                        speak: str = None, input_hint: Union[InputHints, str] = InputHints.accepting_input) -> Activity:
    message = Activity(type=ActivityTypes.message, attachment_layout=attachment_layout, attachments=attachments,
                       input_hint=input_hint)
    if text:
        message.text = text
    if speak:
        message.speak = speak
    return message


class MessageFactory:
    """
    A set of utility functions designed to assist with the formatting of the various message types a
    bot can return.
    """

    @staticmethod
    def text(text: str, speak: str = None, input_hint: Union[InputHints, str] = InputHints.accepting_input) -> Activity:
        """
        Returns a simple text message.

        :Example:
        message = MessageFactory.text('Greetings from example message')
        await context.send_activity(message)

        :param text:
        :param speak:
        :param input_hint:
        :return:
        """
        message = Activity(type=ActivityTypes.message, text=text, input_hint=input_hint)
        if speak:
            message.speak = speak

        return message

    @staticmethod
    def suggested_actions(actions: List[Union[CardAction, str]], text: str = None, speak: str = None,
                          input_hint: Union[InputHints, str] = InputHints.accepting_input) -> Activity:
        """
        Returns a message that includes a set of suggested actions and optional text.

        :Example:
        message = MessageFactory.suggested_actions(['red', 'green', 'blue'], `Choose a color`)
        await context.send_activity(message)

        :param actions:
        :param text:
        :param speak:
        :param input_hint:
        :return:
        """
        actions = SuggestedActions(actions=CardFactory.actions(actions))
        message = Activity(type=ActivityTypes.message, input_hint=input_hint, suggested_actions=actions)
        if text:
            message.text = text
        if speak:
            message.speak = speak
        return message

    @staticmethod
    def attachment(attachment: Attachment, text: str = None, speak: str = None,
                   input_hint: Union[InputHints, str] = None):
        """
        Returns a single message activity containing an attachment.

        :Example:
        message = MessageFactory.attachment(CardFactory.heroCard('White T-Shirt',
                                                                 ['https://example.com/whiteShirt.jpg'],
                                                                 ['buy']))
        await context.send_activity(message)

        :param attachment:
        :param text:
        :param speak:
        :param input_hint:
        :return:
        """
        return attachment_activity(AttachmentLayoutTypes.list, [attachment], text, speak, input_hint)

    @staticmethod
    def list(attachments: List[Attachment], text: str = None, speak: str = None,
             input_hint: Union[InputHints, str] = None) -> Activity:
        """
        Returns a message that will display a set of attachments in list form.

        :Example:
        message = MessageFactory.list([CardFactory.hero_card('title1', ['imageUrl1'], ['button1']),
                                       CardFactory.hero_card('title2', ['imageUrl2'], ['button2']),
                                       CardFactory.hero_card('title3', ['imageUrl3'], ['button3'])])
        await context.send_activity(message)

        :param attachments:
        :param text:
        :param speak:
        :param input_hint:
        :return:
        """
        return attachment_activity(AttachmentLayoutTypes.list, attachments, text, speak, input_hint)

    @staticmethod
    def carousel(attachments: List[Attachment], text: str = None, speak: str = None,
                 input_hint: Union[InputHints, str] = None) -> Activity:
        """
        Returns a message that will display a set of attachments using a carousel layout.

        :Example:
        message = MessageFactory.carousel([CardFactory.hero_card('title1', ['imageUrl1'], ['button1']),
                                           CardFactory.hero_card('title2', ['imageUrl2'], ['button2']),
                                           CardFactory.hero_card('title3', ['imageUrl3'], ['button3'])])
        await context.send_activity(message)

        :param attachments:
        :param text:
        :param speak:
        :param input_hint:
        :return:
        """
        return attachment_activity(AttachmentLayoutTypes.carousel, attachments, text, speak, input_hint)

    @staticmethod
    def content_url(url: str, content_type: str, name: str = None, text: str = None, speak: str = None,
                    input_hint: Union[InputHints, str] = None):
        """
        Returns a message that will display a single image or video to a user.

        :Example:
        message = MessageFactory.content_url('https://example.com/hawaii.jpg', 'image/jpeg',
                                             'Hawaii Trip', 'A photo from our family vacation.')
        await context.send_activity(message)

        :param url:
        :param content_type:
        :param name:
        :param text:
        :param speak:
        :param input_hint:
        :return:
        """
        attachment = Attachment(content_type=content_type, content_url=url)
        if name:
            attachment.name = name
        return attachment_activity(AttachmentLayoutTypes.list, [attachment], text, speak, input_hint)
