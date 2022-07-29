# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from botbuilder.core import CardFactory
from botbuilder.schema import Activity, ActivityTypes, CardAction, HeroCard

from ..models import QueryResult


class QnACardBuilder:
    """
    Message activity card builder for QnAMaker dialogs.
    """

    @staticmethod
    def get_suggestions_card(
        suggestions: List[str], card_title: str, card_no_match: str
    ) -> Activity:
        """
        Get active learning suggestions card.
        """

        if not suggestions:
            raise TypeError("suggestions list is required")

        if not card_title:
            raise TypeError("card_title is required")

        if not card_no_match:
            raise TypeError("card_no_match is required")

        # Add all suggestions
        button_list = [
            CardAction(value=suggestion, type="imBack", title=suggestion)
            for suggestion in suggestions
        ]

        # Add No match text
        button_list.append(
            CardAction(value=card_no_match, type="imBack", title=card_no_match)
        )

        attachment = CardFactory.hero_card(HeroCard(buttons=button_list))

        return Activity(
            type=ActivityTypes.message, text=card_title, attachments=[attachment]
        )

    @staticmethod
    def get_qna_prompts_card(result: QueryResult, card_no_match_text: str) -> Activity:
        """
        Get active learning suggestions card.
        """

        if not result:
            raise TypeError("result is required")

        if not card_no_match_text:
            raise TypeError("card_no_match_text is required")

        # Add all prompts
        button_list = [
            CardAction(
                value=prompt.display_text,
                type="imBack",
                title=prompt.display_text,
            )
            for prompt in result.context.prompts
        ]

        attachment = CardFactory.hero_card(HeroCard(buttons=button_list))

        return Activity(
            type=ActivityTypes.message, text=result.answer, attachments=[attachment]
        )
