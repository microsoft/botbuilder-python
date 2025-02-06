# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model
from botbuilder.schema.sharepoint import AceData
from botbuilder.schema.sharepoint.actions import OnCardSelectionAction
from botbuilder.schema.sharepoint.card_view import CardViewParameters


class CardViewResponse(Model):
    """
    SharePoint Card View Data object.

    :param ace_date: AceData for the card view of type.
    :type ace_date: AceData
    :param card_view_parameters: Card view configuration.
    :type card_view_parameters: CardViewParameters
    :param on_card_selection: Action to invoke when the card is selected.
    :type on_card_selection: OnCardSelectionAction
    :param view_id: The ID of the view.
    :type view_id: str
    """

    _attribute_map = {
        "ace_date": {"key": "aceDate", "type": "AceData"},
        "card_view_parameters": {
            "key": "cardViewParameters",
            "type": "CardViewParameters",
        },
        "on_card_selection": {
            "key": "onCardSelection",
            "type": "OnCardSelectionAction",
        },
        "view_id": {"key": "viewId", "type": "str"},
    }

    def __init__(
        self,
        *,
        ace_date: AceData = None,
        card_view_parameters: CardViewParameters = None,
        on_card_selection: OnCardSelectionAction = None,
        view_id: str = None,
        **kwargs
    ) -> None:
        super(CardViewResponse, self).__init__(**kwargs)
        self.ace_date = ace_date
        self.card_view_parameters = card_view_parameters
        self.on_card_selection = on_card_selection
        self.view_id = view_id
