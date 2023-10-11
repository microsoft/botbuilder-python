# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from msrest.serialization import Model
from .query_result import QueryResult


class QueryResults(Model):
    """Contains answers for a user query."""

    _attribute_map = {
        "answers": {"key": "answers", "type": "[QueryResult]"},
        "active_learning_enabled": {"key": "activeLearningEnabled", "type": "bool"},
    }

    def __init__(
        self, answers: List[QueryResult], active_learning_enabled: bool = None, **kwargs
    ):
        """
        Parameters:
        -----------

        answers: The answers for a user query.

        active_learning_enabled: The active learning enable flag.
        """
        super().__init__(**kwargs)
        self.answers = answers
        self.active_learning_enabled = active_learning_enabled
