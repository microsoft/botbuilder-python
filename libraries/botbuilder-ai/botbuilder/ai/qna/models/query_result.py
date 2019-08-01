# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from .metadata import Metadata


class QueryResult:
    """ Represents an individual result from a knowledge base query. """

    def __init__(
        self,
        questions: List[str],
        answer: str,
        score: float,
        metadata: object = None,
        source: str = None,
        id: int = None,  # pylint: disable=invalid-name
    ):
        """
        Parameters:
        -----------

        questions: The list of questions indexed in the QnA Service for the given answer (if any).

        answer: Answer from the knowledge base.

        score: Confidence on a scale from 0.0 to 1.0 that the answer matches the user's intent.

        metadata: Metadata associated with the answer (if any).

        source: The source from which the QnA was extracted (if any).

        id: The index of the answer in the knowledge base. V3 uses 'qnaId', V4 uses 'id' (if any).
        """
        self.questions = questions
        self.answer = answer
        self.score = score
        self.metadata = list(map(lambda meta: Metadata(**meta), metadata))
        self.source = source
        self.id = id  # pylint: disable=invalid-name
