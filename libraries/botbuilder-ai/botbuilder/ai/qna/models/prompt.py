# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class Prompt(Model):
    """Prompt Object."""

    _attribute_map = {
        "display_order": {"key": "displayOrder", "type": "int"},
        "qna_id": {"key": "qnaId", "type": "int"},
        "qna": {"key": "qna", "type": "object"},
        "display_text": {"key": "displayText", "type": "str"},
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.display_order = kwargs.get("display_order", None)
        self.qna_id = kwargs.get("qna_id", None)
        self.display_text = kwargs.get("display_text", None)
        self.qna = kwargs.get("qna", None)
