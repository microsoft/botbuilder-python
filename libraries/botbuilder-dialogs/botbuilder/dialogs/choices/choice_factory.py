# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.core import CardFactory, MessageFactory
from botbuilder.schema import ActionTypes, Activity, CardAction, HeroCard, InputHints

from . import Channel, Choice, ChoiceFactoryOptions


class ChoiceFactory:
    @staticmethod
    def for_channel(
        channel_id: str,
        choices: List[Choice],
        text: str = None,
        speak: str = None,
        options: ChoiceFactoryOptions = None,
    ) -> Activity:
        if channel_id is None:
            channel_id = ""

        if choices is None:
            choices = []

        # Find maximum title length
        max_title_length = 0
        for choice in choices:
            if choice.action is not None and choice.action.title not in (None, ""):
                l = len(choice.action.title)
            else:
                l = len(choice.value)

            if l > max_title_length:
                max_title_length = l

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
        elif not long_titles and supports_suggested_actions:
            # We always prefer showing choices using suggested actions. If the titles are too long, however,
            # we'll have to show them as a text list.
            return ChoiceFactory.suggested_action(choices, text, speak)
        elif not long_titles and len(choices) <= 3:
            # If the titles are short and there are 3 or less choices we'll use an inline list.
            return ChoiceFactory.inline(choices, text, speak, options)
        else:
            # Show a numbered list.
            return List(choices, text, speak, options)

    @staticmethod
    def inline(
        choices: List[Choice],
        text: str = None,
        speak: str = None,
        options: ChoiceFactoryOptions = None,
    ) -> Activity:
        if choices is None:
            choices = []

        if options is None:
            options = ChoiceFactoryOptions()

        opt = ChoiceFactoryOptions(
            inline_separator=options.inline_separator or ", ",
            inline_or=options.inline_or or " or ",
            inline_or_more=options.inline_or_more or ", or ",
            include_numbers=options.include_numbers or True,
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
        choices: List[Choice],
        text: str = None,
        speak: str = None,
        options: ChoiceFactoryOptions = None,
    ):
        if choices is None:
            choices = []
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
        # Return activity with choices as suggested actions
        return MessageFactory.suggested_actions(
            ChoiceFactory._extract_actions(choices),
            text,
            speak,
            InputHints.expecting_input,
        )

    @staticmethod
    def hero_card(
        choices: List[Choice], text: str = None, speak: str = None
    ) -> Activity:
        attachment = CardFactory.hero_card(
            HeroCard(text=text, buttons=ChoiceFactory._extract_actions(choices))
        )

        # Return activity with choices as HeroCard with buttons
        return MessageFactory.attachment(
            attachment, None, speak, InputHints.expecting_input
        )

    @staticmethod
    def _to_choices(choices: List[str]) -> List[Choice]:
        if choices is None:
            return []
        else:
            return [Choice(value=choice.value) for choice in choices]

    @staticmethod
    def _extract_actions(choices: List[Choice]) -> List[CardAction]:
        if choices is None:
            choices = []
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
