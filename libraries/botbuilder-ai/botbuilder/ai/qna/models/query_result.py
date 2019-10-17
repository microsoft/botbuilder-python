# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from msrest.serialization import Model
from .metadata import Metadata
from .qna_response_context import QnAResponseContext


class QueryResult(Model):
    """ Represents an individual result from a knowledge base query. """

    _attribute_map = {
        "questions": {"key": "questions", "type": "[str]"},
        "answer": {"key": "answer", "type": "str"},
        "score": {"key": "score", "type": "float"},
        "metadata": {"key": "metadata", "type": "object"},
        "source": {"key": "source", "type": "str"},
        "id": {"key": "id", "type": "int"},
        "context": {"key": "context", "type": "object"},
    }

    def __init__(
        self,
        *,
        questions: List[str],
        answer: str,
        score: float,
        metadata: object = None,
        source: str = None,
        id: int = None,  # pylint: disable=invalid-name
        context: QnAResponseContext = None,
        **kwargs
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

        context: The context from which the QnA was extracted.
        """
        super(QueryResult, self).__init__(**kwargs)
        self.questions = questions
        self.answer = answer
        self.score = score
        self.metadata = list(map(lambda meta: Metadata(**meta), metadata))
        self.source = source
        self.context = QnAResponseContext(**context) if context is not None else None
        self.id = id  # pylint: disable=invalid-name
