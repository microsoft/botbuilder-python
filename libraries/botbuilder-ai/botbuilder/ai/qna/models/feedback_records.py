# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from .feedback_record import FeedbackRecord

class FeedbackRecords:
    """ Active learning feedback records. """
    def __init__(self, records: List[FeedbackRecord]):
        """
        Parameter(s):
        -------------

        records: List of feedback records.
        """
        self.records = records
