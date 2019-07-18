# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from .metadata import Metadata
from .query_result import QueryResult


class QueryResults:
    """ Contains answers for a user query. """

    def __init__(self, answers: List[QueryResult]):
        """
        Parameters:
        -----------

        answers: The answers for a user query.
        """
        self.answers = answers
