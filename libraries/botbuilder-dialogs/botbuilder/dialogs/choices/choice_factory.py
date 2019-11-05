# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List, Union

from botbuilder.core import CardFactory, MessageFactory
from botbuilder.schema import ActionTypes, Activity, CardAction, HeroCard, InputHints

from . import Channel, Choice, ChoiceFactoryOptions


class ChoiceFactory:
    """
    Assists with formatting a message activity that contains a list of choices.
    """

    @staticmethod
    def for_channel(
        channel_id: str,
        choices: List[Union[str, Choice]],
        text: str = None,
        speak: str = None,
        options: ChoiceFactoryOptions = None,
    ) -> Activity:
        """
        Creates a message activity that includes a list of choices formatted based on the
         capabilities of a given channel.

        Parameters:
        ----------
        channel_id: A channel ID.
        choices: List of choices to render
        text: (Optional) Text of the message to send.
        speak (Optional) SSML. Text to be spoken by your bot on a speech-enabled channel.
        """
        if channel_id is None:
            channel_id = ""

        choices = ChoiceFactory._to_choices(choices)

        # Find maximum title length
        max_title_length = 0
        for choice in choices:
            if choice.action is not None and choice.action.title not in (None, ""):
                size = len(choice.action.title)
            else:
                size = len(choice.value)

            if size > max_title_length:
                max_title_length = size

        # Determine list style
        supports_suggested_actions = Channel.supports_suggested_actions(
            channel_id, len(choices)
        )
        supports_card_actions = Channel.supports_card_actions(channel_id, len(choices))
        max_action_title_length = Channel.max_action_title_length(channel_id)
        long_titles = max_title_length > max_action_title_length

        if not long_titles and not supports_suggested_actions and supports_card_actions:
            # SuggestedActions is the preferred approach, but for channels that don't
            # support them (e.g. Teams, Cortana) we should use a HeroCard with CardActions
            return ChoiceFactory.hero_card(choices, text, speak)
        if not long_titles and supports_suggested_actions:
            # We always prefer showing choices using suggested actions. If the titles are too long, however,
            # we'll have to show them as a text list.
            return ChoiceFactory.suggested_action(choices, text, speak)
        if not long_titles and len(choices) <= 3:
            # If the titles are short and there are 3 or less choices we'll use an inline list.
            return ChoiceFactory.inline(choices, text, speak, options)
        # Show a numbered list.
        return ChoiceFactory.list_style(choices, text, speak, options)

    @staticmethod
    def inline(
        choices: List[Union[str, Choice]],
        text: str = None,
        speak: str = None,
        options: ChoiceFactoryOptions = None,
    ) -> Activity:
        """
        Creates a message activity that includes a list of choices formatted as an inline list.

        Parameters:
        ----------
        choices: The list of choices to render.
        text: (Optional) The text of the message to send.
        speak: (Optional) SSML. Text to be spoken by your bot on a speech-enabled channel.
        options: (Optional) The formatting options to use to tweak rendering of list.
        """
        choices = ChoiceFactory._to_choices(choices)

        if options is None:
            options = ChoiceFactoryOptions()

        opt = ChoiceFactoryOptions(
            inline_separator=options.inline_separator or ", ",
            inline_or=options.inline_or or " or ",
            inline_or_more=options.inline_or_more or ", or ",
            include_numbers=(
                options.include_numbers if options.include_numbers is not None else True
            ),
        )

        # Format list of choices
        connector = ""
        txt_builder: List[str] = [text]
        txt_builder.append(" ")
        for index, choice in enumerate(choices):
            title = (
                choice.action.title
                if (choice.action is not None and choice.action.title is not None)
                else choice.value
            )
            txt_builder.append(connector)
            if opt.include_numbers is True:
                txt_builder.append("(")
                txt_builder.append(f"{index + 1}")
                txt_builder.append(") ")

            txt_builder.append(title)
            if index == (len(choices) - 2):
                connector = opt.inline_or if index == 0 else opt.inline_or_more
                connector = connector or ""
            else:
                connector = opt.inline_separator or ""

        # Return activity with choices as an inline list.
        return MessageFactory.text(
            "".join(txt_builder), speak, InputHints.expecting_input
        )

    @staticmethod
    def list_style(
        choices: List[Union[str, Choice]],
        text: str = None,
        speak: str = None,
        options: ChoiceFactoryOptions = None,
    ):
        """
        Creates a message activity that includes a list of choices formatted as a numbered or bulleted list.

        Parameters:
        ----------

        choices: The list of choices to render.

        text: (Optional) The text of the message to send.

        speak: (Optional) SSML. Text to be spoken by your bot on a speech-enabled channel.

        options: (Optional) The formatting options to use to tweak rendering of list.
        """
        choices = ChoiceFactory._to_choices(choices)
        if options is None:
            options = ChoiceFactoryOptions()

        if options.include_numbers is None:
            include_numbers = True
        else:
            include_numbers = options.include_numbers

        # Format list of choices
        connector = ""
        txt_builder = [text]
        txt_builder.append("\n\n   ")

        for index, choice in enumerate(choices):
            title = (
                choice.action.title
                if choice.action is not None and choice.action.title is not None
                else choice.value
            )

            txt_builder.append(connector)
            if include_numbers:
                txt_builder.append(f"{index + 1}")
                txt_builder.append(". ")
            else:
                txt_builder.append("- ")

            txt_builder.append(title)
            connector = "\n   "

        # Return activity with choices as a numbered list.
        txt = "".join(txt_builder)
        return MessageFactory.text(txt, speak, InputHints.expecting_input)

    @staticmethod
    def suggested_action(
        choices: List[Choice], text: str = None, speak: str = None
    ) -> Activity:
        """
        Creates a message activity that includes a list of choices that have been added as suggested actions.
        """
        # Return activity with choices as suggested actions
        return MessageFactory.suggested_actions(
            ChoiceFactory._extract_actions(choices),
            text,
            speak,
            InputHints.expecting_input,
        )

    @staticmethod
    def hero_card(
        choices: List[Union[Choice, str]], text: str = None, speak: str = None
    ) -> Activity:
        """
        Creates a message activity that includes a lsit of coices that have been added as `HeroCard`'s
        """
        attachment = CardFactory.hero_card(
            HeroCard(text=text, buttons=ChoiceFactory._extract_actions(choices))
        )

        # Return activity with choices as HeroCard with buttons
        return MessageFactory.attachment(
            attachment, None, speak, InputHints.expecting_input
        )

    @staticmethod
    def _to_choices(choices: List[Union[str, Choice]]) -> List[Choice]:
        """
        Takes a list of strings and returns them as [`Choice`].
        """
        if choices is None:
            return []
        return [
            Choice(value=choice) if isinstance(choice, str) else choice
            for choice in choices
        ]

    @staticmethod
    def _extract_actions(choices: List[Union[str, Choice]]) -> List[CardAction]:
        if choices is None:
            choices = []
        choices = ChoiceFactory._to_choices(choices)
        card_actions: List[CardAction] = []
        for choice in choices:
            if choice.action is not None:
                card_action = choice.action
            else:
                card_action = CardAction(
                    type=ActionTypes.im_back, value=choice.value, title=choice.value
                )

            card_actions.append(card_action)

        return card_actions
