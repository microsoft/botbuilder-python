# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from msrest.serialization import Model
from botbuilder.schema.sharepoint.card_view import (
    BaseCardComponent,
    CardBarComponent,
    CardButtonComponent,
    CardImage,
    CardSearchBoxComponent,
    CardSearchFooterComponent,
    CardTextComponent,
    CardTextInputComponent,
)


class CardViewParameters(Model):
    """
    Adaptive Card Extension Card View Parameters.

    :param card_view_type: The type of card view.
    :type card_view_type: str
    :param image: The image to display on the card view.
    :type image: CardImage
    :param card_bar: The card bar to display on the card view.
    :type card_bar: list[CardBarComponent]
    :param header: The header to display on the card view.
    :type header: list[BaseCardComponent]
    :param body: The body to display on the card view.
    :type body: list[BaseCardComponent]
    :param footer: The footer to display on the card view.
    :type footer: list[BaseCardComponent]
    """

    _attribute_map = {
        "card_view_type": {"key": "cardViewType", "type": "str"},
        "image": {"key": "image", "type": "CardImage"},
        "card_bar": {"key": "cardBar", "type": "[CardBarComponent]"},
        "header": {"key": "header", "type": "[BaseCardComponent]"},
        "body": {"key": "body", "type": "[BaseCardComponent]"},
        "footer": {"key": "footer", "type": "[BaseCardComponent]"},
    }

    def __init__(
        self,
        *,
        card_view_type: str = None,
        image: CardImage = None,
        card_bar: List[CardBarComponent] = None,
        header: List[BaseCardComponent] = None,
        body: List[BaseCardComponent] = None,
        footer: List[BaseCardComponent] = None,
        **kwargs
    ) -> None:
        super(CardViewParameters, self).__init__(**kwargs)
        self.card_view_type = card_view_type
        self.image = image
        self.card_bar = card_bar
        self.header = header
        self.body = body
        self.footer = footer

    @staticmethod
    def basic_card_view_parameters(
        card_bar: "CardBarComponent",
        header: "CardTextComponent",
        footer: List["BaseCardComponent"],
    ) -> "CardViewParameters":
        if card_bar is None:
            raise ValueError("card_bar cannot be None")
        if header is None:
            raise ValueError("header cannot be None")
        CardViewParameters.validate_generic_card_view_footer_configuration(footer)

        return CardViewParameters(
            card_view_type="text", card_bar=[card_bar], header=[header], footer=footer
        )

    @staticmethod
    def primary_text_card_view_parameters(
        card_bar: "CardBarComponent",
        header: "CardTextComponent",
        body: "CardTextComponent",
        footer: List["BaseCardComponent"],
    ) -> "CardViewParameters":
        if card_bar is None:
            raise ValueError("card_bar cannot be None")
        if header is None:
            raise ValueError("header cannot be None")
        if body is None:
            raise ValueError("body cannot be None")
        CardViewParameters.validate_generic_card_view_footer_configuration(footer)

        return CardViewParameters(
            card_view_type="text",
            card_bar=[card_bar],
            header=[header],
            body=[body],
            footer=footer,
        )

    @staticmethod
    def image_card_view_parameters(
        card_bar: "CardBarComponent",
        header: "CardTextComponent",
        footer: List["BaseCardComponent"],
        image: "CardImage",
    ) -> "CardViewParameters":
        if card_bar is None:
            raise ValueError("card_bar cannot be None")
        if header is None:
            raise ValueError("header cannot be None")
        if image is None:
            raise ValueError("image cannot be None")
        CardViewParameters.validate_generic_card_view_footer_configuration(footer)

        return CardViewParameters(
            card_view_type="text",
            card_bar=[card_bar],
            header=[header],
            image=image,
            footer=footer,
        )

    @staticmethod
    def text_input_card_view_parameters(
        card_bar: "CardBarComponent",
        header: "CardTextComponent",
        body: "CardTextInputComponent",
        footer: List["CardButtonComponent"],
        image: "CardImage" = None,
    ) -> "CardViewParameters":
        if card_bar is None:
            raise ValueError("card_bar cannot be None")
        if header is None:
            raise ValueError("header cannot be None")
        if body is None:
            raise ValueError("body cannot be None")
        if len(footer) > 2:
            raise ValueError("Card view footer must contain up to two buttons.")

        return CardViewParameters(
            card_view_type="textInput",
            card_bar=[card_bar],
            header=[header],
            body=[body],
            image=image,
            footer=footer,
        )

    @staticmethod
    def search_card_view_parameters(
        card_bar: "CardBarComponent",
        header: "CardTextComponent",
        body: "CardSearchBoxComponent",
        footer: "CardSearchFooterComponent",
    ) -> "CardViewParameters":
        if card_bar is None:
            raise ValueError("card_bar cannot be None")
        if header is None:
            raise ValueError("header cannot be None")
        if body is None:
            raise ValueError("body cannot be None")
        if footer is None:
            raise ValueError("footer cannot be None")

        return CardViewParameters(
            card_view_type="search",
            card_bar=[card_bar],
            header=[header],
            body=[body],
            footer=[footer],
        )

    @staticmethod
    def sign_in_card_view_parameters(
        card_bar: "CardBarComponent",
        header: "CardTextComponent",
        body: "CardTextComponent",
        footer: "CardButtonComponent",
    ) -> "CardViewParameters":
        if card_bar is None:
            raise ValueError("card_bar cannot be None")
        if header is None:
            raise ValueError("header cannot be None")
        if body is None:
            raise ValueError("body cannot be None")
        if footer is None:
            raise ValueError("footer cannot be None")

        return CardViewParameters(
            card_view_type="signIn",
            card_bar=[card_bar],
            header=[header],
            body=[body],
            footer=[footer],
        )

    @staticmethod
    def validate_generic_card_view_footer_configuration(
        footer: List[BaseCardComponent],
    ) -> None:
        """
        Validates the generic card view footer configuration.

        :param footer: The footer to validate.
        :type footer: list[BaseCardComponent]
        :raises ValueError: The footer is invalid.
        """
        if footer is None or len(footer) == 0:
            return
        if len(footer) > 2:
            raise ValueError(
                "Card view footer must contain up to two buttons or text input."
            )
        if len(footer) == 2 and not all(
            isinstance(comp, CardButtonComponent) for comp in footer
        ):
            raise ValueError("Both footer components must be buttons if there are two.")
        if len(footer) == 1 and not isinstance(
            footer[0], (CardButtonComponent, CardTextInputComponent)
        ):
            raise ValueError("Single footer component must be a button or text input.")
