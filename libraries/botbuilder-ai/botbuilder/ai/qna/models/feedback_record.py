# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class FeedbackRecord(Model):
    """Active learning feedback record."""

    _attribute_map = {
        "user_id": {"key": "userId", "type": "str"},
        "user_question": {"key": "userQuestion", "type": "str"},
        "qna_id": {"key": "qnaId", "type": "int"},
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = kwargs.get("user_id", None)
        self.user_question = kwargs.get("user_question", None)
        self.qna_id = kwargs.get("qna_id", None)
