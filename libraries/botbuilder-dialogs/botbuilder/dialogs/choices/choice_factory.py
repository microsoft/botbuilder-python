# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List, Union
from botbuilder.core import MessageFactory
from botbuilder.schema import ActionTypes, Activity, CardAction, InputHints

from .choices import Choice
from .channel import Channel


class ChoiceFactoryOptions:
    def __init__(self, inline_separator: str = ", ", inline_or: str = " or ",
                 inline_or_more: str = ", or ", include_numbers: bool = True):
        """Additional options used to tweak the formatting of choice lists.
        :param inline_separator:
        :param inline_or:
        :param inline_or_more:
        :param include_numbers:
        """

        """(Optional) character used to separate individual choices when there are more than 2 choices.
        The default value is `", "`."""
        self.inline_separator = inline_separator

        """(Optional) separator inserted between the choices when their are only 2 choices. The default
        value is `" or "`."""
        self.inline_or = inline_or

        """(Optional) separator inserted between the last 2 choices when their are more than 2 choices.
        The default value is `", or "`."""
        self.inline_or_more = inline_or_more

        """(Optional) if `true`, inline and list style choices will be prefixed with the index of the
        choice as in "1. choice". If `false`, the list style will use a bulleted list instead. The 
        default value is `true`."""
        self.include_numbers = include_numbers


class ChoiceFactory:
    """A set of utility functions to assist with the formatting a 'message' activity containing a list
    of choices.
    """

    @staticmethod
    def for_channel(channel_id: str, choices: List[Choice] = None,
                    text: str = None, speak: str = None,
                    options: ChoiceFactoryOptions = None) -> Activity:
        """
        Returns a 'message' activity containing a list of choices that has been automatically
        formatted based on the capabilities of a given channel.

        @remarks
        The algorithm prefers to format the supplied list of choices as suggested actions but can
        decide to use a text based list if suggested actions aren't natively supported by the
        channel, there are too many choices for the channel to display, or the title of any choice
        is too long.

        If the algorithm decides to use a list it will use an inline list if there are 3 or less
        choices and all have short titles. Otherwise, a numbered list is used.
        :param channel_id:
        :param choices:
        :param text:
        :param speak:
        :param options:
        :return:
        """

        # Find maximum title length
        max_title_length = 0
        for choice in choices:
            length = (len(choice.action.title) if choice.action is not None and choice.action.title is not None else
                      len(choice.value))
            if length > max_title_length:
                max_title_length = length

        # Determine list style
        supports_suggested_actions = Channel.supports_suggested_actions(channel_id, len(choices))
        supports_card_actions = Channel.supports_card_actions(channel_id, len(choices))
        max_action_title_length = Channel.max_action_title_length(channel_id)
        has_message_feed = Channel.has_message_feed(channel_id)
        long_titles = max_title_length > max_action_title_length

        if not long_titles and (supports_suggested_actions or (not has_message_feed and supports_card_actions)):
            # We always prefer showing choices using suggested actions. If the titles are too long, however,
            # we'll have to show them as a text list.
            return ChoiceFactory.suggested_action(choices, text, speak)
        elif not long_titles and len(choices) <= 3:
            # If the titles are short and there are 3 or less choices we'll use an inline list.
            return ChoiceFactory.inline(choices, text, speak, options)
        else:
            return ChoiceFactory.list(choices, text, speak, options)

    @staticmethod
    def inline(choices: List[Choice], text: str = '',
               speak: str = '', options: ChoiceFactoryOptions = ChoiceFactoryOptions()) -> Activity:
        """Returns a 'message' activity containing a list of choices that has been formatted as an
        inline list.

        @remarks
        This example generates a message text of "Pick a color: (1. red, 2. green, or 3. blue)":
        :param choices:
        :param text:
        :param speak:
        :param options:
        :return:
        """
        choices = choices or []

        # Format list of choices.
        connector = ''
        txt = text or ''
        txt += ' '

        for index, choice in enumerate(choices):
            title = (choice.action.title if hasattr(choice.action, 'title') and choice.action.title is not None else
                     choice.value)
            txt += connector
            if options.include_numbers:
                txt += f"({str(index +1)}) "
            txt += f"{title}"
            if index == (len(choices) - 2):
                connector = options.inline_or if index == 0 else options.inline_or_more
                connector = connector or ''
            else:
                connector = options.inline_separator or ''
            txt += ""

        # Return activity with choices as an inline list.
        return MessageFactory.text(txt, speak, InputHints.expecting_input)

    @staticmethod
    def list(choices: List[Choice], text: str = None,
             speak: str = None, options: ChoiceFactoryOptions = ChoiceFactoryOptions()) -> Activity:
        """Returns a 'message' activity containing a list of choices that has been formatted as an
        numbered or bulleted list.

        :param choices:
        :param text:
        :param speak:
        :param options:
        :return:
        """

        # Format list of choices.
        connector = ''
        txt = text or ''
        txt += '\n\n   '
        for index, choice in enumerate(choices):
            title = (choice.action.title if hasattr(choice.action, 'title') and choice.action.title is not None else
                     choice.value)
            txt += f"{connector}{str(index + 1) + '. ' if options.include_numbers else '- '}{title}"
            connector = '\n   '

        # Return activity with choices as a numbered list.
        return MessageFactory.text(txt, speak, InputHints.expecting_input)

    @staticmethod
    def suggested_action(choices: List[Choice], text: str = '', speak: str = None) -> Activity:
        """Returns a 'message' activity containing a list of choices that have been added as suggested actions.
        :param choices:
        :param text:
        :param speak:
        :return:
        """
        # Map choices to actions
        actions = []
        for choice in choices:
            if choice.action:
                actions.append(choice.action)
            else:
                actions.append(CardAction(value=choice.value,
                                          title=choice.value,
                                          type=ActionTypes.im_back))

        return MessageFactory.suggested_actions(actions, text, speak, InputHints.expecting_input)

    @staticmethod
    def to_choices(choices: List[Union[str, Choice]]) -> List[Choice]:
        """
        Takes a mixed list of `string` and `Choice` based choices and returns them as a `List[Choice]`.
        Will raise a TypeError if it finds a choice that is not a str or an instance of Choice.
        :param choices:
        :return:
        """
        prepared_choices = []

        for (idx, choice) in enumerate(choices):
            # If choice is a str, convert it to a Choice.
            if type(choice) == str:
                prepared_choices.append(Choice(choice))

            # If the choice is an instance of Choice, do nothing.
            elif isinstance(choice, Choice):
                prepared_choices.append(choice)
            else:
                raise TypeError(f'ChoiceFactory.to_choices(): choice at index {idx} is not of type str or instance of '
                                'Choice.')

        return prepared_choices
