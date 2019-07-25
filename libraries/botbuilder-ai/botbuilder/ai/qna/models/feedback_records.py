# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from msrest.serialization import Model

from .feedback_record import FeedbackRecord


class FeedbackRecords(Model):
    """ Active learning feedback records. """

    _attribute_map = {"records": {"key": "records", "type": "[FeedbackRecord]"}}

    def __init__(self, records: List[FeedbackRecord], **kwargs):
        """
        Parameter(s):
        -------------

        records: List of feedback records.
        """

        super().__init__(**kwargs)

        self.records = records
