# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.schema import Activity
from .metadata import Metadata
from .query_result import QueryResult
from .qna_request_context import QnARequestContext


class QnAMakerTraceInfo:
    """ Represents all the trace info that we collect from the QnAMaker Middleware. """

    def __init__(
        self,
        message: Activity,
        query_results: List[QueryResult],
        knowledge_base_id: str,
        score_threshold: float,
        top: int,
        strict_filters: List[Metadata],
        context: QnARequestContext = None,
        qna_id: int = None,
    ):
        """
        Parameters:
        -----------

        message: Message which instigated the query to QnA Maker.

        query_results: Results that QnA Maker returned.

        knowledge_base_id: ID of the knowledge base that is being queried.

        score_threshold: The minimum score threshold, used to filter returned results.

        top: Number of ranked results that are asked to be returned.

        strict_filters: Filters used on query.

        context: (Optional) The context from which the QnA was extracted.

        qna_id: (Optional) Id of the current question asked.
        """
        self.message = message
        self.query_results = query_results
        self.knowledge_base_id = knowledge_base_id
        self.score_threshold = score_threshold
        self.top = top
        self.strict_filters = strict_filters
        self.context = context
        self.qna_id = qna_id
