# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class FeedbackRecord(Model):
    """ Active learning feedback record. """

    _attribute_map = {
        "user_id": {"key": "userId", "type": "str"},
        "user_question": {"key": "userQuestion", "type": "str"},
        "qna_id": {"key": "qnaId", "type": "int"},
    }

    def __init__(self, user_id: str, user_question: str, qna_id: int, **kwargs):
        """
        Parameters:
        -----------

        user_id: ID of the user.

        user_question: User question.

        qna_id: QnA ID.
        """

        super().__init__(**kwargs)

        self.user_id = user_id
        self.user_question = user_question
        self.qna_id = qna_id
