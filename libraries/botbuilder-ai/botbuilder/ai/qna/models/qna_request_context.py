# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class QnARequestContext(Model):
    """
    The context associated with QnA.
    Used to mark if the current prompt is relevant with a previous question or not.
    """

    _attribute_map = {
        "previous_qna_id": {"key": "previousQnAId", "type": "int"},
        "previous_user_query": {"key": "previousUserQuery", "type": "string"},
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.previous_qna_id = kwargs.get("previous_qna_id", None)
        self.previous_user_query = kwargs.get("previous_user_query", None)
