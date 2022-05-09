# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class FeedbackRecords(Model):
    """Active learning feedback records."""

    _attribute_map = {"records": {"key": "records", "type": "[FeedbackRecord]"}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.records = kwargs.get("records", None)
