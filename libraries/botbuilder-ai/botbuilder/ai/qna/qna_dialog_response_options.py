# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import Activity


class QnADialogResponseOptions:
    def __init__(
        self,
        active_learning_card_title: str = None,
        card_no_match_text: str = None,
        no_answer: Activity = None,
        card_no_match_response: Activity = None,
    ):
        self.active_learning_card_title = active_learning_card_title
        self.card_no_match_text = card_no_match_text
        self.no_answer = no_answer
        self.card_no_match_response = card_no_match_response
