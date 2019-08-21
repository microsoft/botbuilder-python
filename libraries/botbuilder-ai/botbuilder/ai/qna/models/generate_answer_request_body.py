# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from msrest.serialization import Model

from .metadata import Metadata
from .qna_request_context import QnARequestContext


class GenerateAnswerRequestBody(Model):
    """ Question used as the payload body for QnA Maker's Generate Answer API. """

    _attribute_map = {
        "question": {"key": "question", "type": "str"},
        "top": {"key": "top", "type": "int"},
        "score_threshold": {"key": "scoreThreshold", "type": "float"},
        "strict_filters": {"key": "strictFilters", "type": "[Metadata]"},
        "context": {"key": "context", "type": "QnARequestContext"},
    }

    def __init__(
        self,
        question: str,
        top: int,
        score_threshold: float,
        strict_filters: List[Metadata],
        context: QnARequestContext = None,
        **kwargs
    ):
        """
        Parameters:
        -----------

        question: The user question to query against the knowledge base.

        top: Max number of answers to be returned for the question.

        score_threshold: Threshold for answers returned based on score.

        strict_filters: Find only answers that contain these metadata.

        context: Find only answers that contain these metadata.

        """

        super().__init__(**kwargs)

        self.question = question
        self.top = top
        self.score_threshold = score_threshold
        self.strict_filters = strict_filters
        self.context = context or None
