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

    def __init__(
        self, previous_qna_id: int = None, previous_user_query: str = None, **kwargs
    ):
        """
        Parameters:
        -----------

        previous_qna_id: The previous QnA Id that was returned.

        previous_user_query: The previous user query/question.
        """

        super().__init__(**kwargs)

        self.previous_qna_id = previous_qna_id
        self.previous_user_query = previous_user_query
