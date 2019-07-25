# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model
from .feedback_records import FeedbackRecords


class TrainRequestBody(Model):
    """ Class the models the request body that is sent as feedback to the Train API. """

    _attribute_map = {
        "feedback_records": {"key": "feedbackRecords", "type": "FeedbackRecords"}
    }

    def __init__(self, feedback_records: FeedbackRecords, **kwargs):
        """
        Parameters:
        -----------

        feedback_records: List of feedback records.
        """

        super().__init__(**kwargs)

        self.feedback_records = feedback_records
