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
        self,
        *,
        display_order: int,
        qna_id: int,
        display_text: str,
        qna: object = None,
        **kwargs
    ):
        """
        Parameters:
        -----------

        display_order: Index of the prompt - used in ordering of the prompts.

        qna_id: QnA ID.

        display_text: Text displayed to represent a follow up question prompt.

        qna: The QnA object returned from the API (Optional).

        """

        super(Prompt, self).__init__(**kwargs)

        self.display_order = display_order
        self.qna_id = qna_id
        self.display_text = display_text
        self.qna = qna
