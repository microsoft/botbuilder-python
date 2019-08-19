# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class Prompt(Model):
    """ Prompt Object. """

    _attribute_map = {
        "display_order": {"key": "displayOrder", "type": "int"},
        "qna_id": {"key": "qnaId", "type": "int"},
        "qna": {"key": "qna", "type": "object"},
        "display_text": {"key": "displayText", "type": "str"},
    }

    def __init__(
        self, display_order: int, qna_id: int, qna: object, display_text: str, **kwargs
    ):
        """
        Parameters:
        -----------

        display_order: Index of the prompt - used in ordering of the prompts.

        qna_id: QnA ID.

        qna: The QnA object returned from the API (Optional parameter).

        display_text: Text displayed to represent a follow up question prompt.
        """

        super().__init__(**kwargs)

        self.display_order = display_order
        self.qna_id = qna_id
        self.qna = qna
        self.display_text = display_text
