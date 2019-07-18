# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class FeedbackRecord:
    """ Active learning feedback record. """
    def __init__(self, user_id, user_question, qna_id):
        """
        Parameters:
        -----------

        user_id: ID of the user.

        user_question: User question.

        qna_id: QnA ID.        
        """
        self.user_id = user_id
        self.user_question = user_question
        self.qna_id = qna_id
