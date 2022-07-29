# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class TrainRequestBody(Model):
    """Class the models the request body that is sent as feedback to the Train API."""

    _attribute_map = {
        "feedback_records": {"key": "feedbackRecords", "type": "[FeedbackRecord]"}
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.feedback_records = kwargs.get("feedback_records", None)
