# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .models import Metadata, QnARequestContext
from .models.ranker_types import RankerTypes
from .models.join_operator import JoinOperator


class QnAMakerOptions:
    """
    Defines options used to configure a `QnAMaker` instance.

    remarks:
    --------
        All parameters are optional.
    """

    def __init__(
        self,
        score_threshold: float = 0.0,
        timeout: int = 0,
        top: int = 0,
        strict_filters: [Metadata] = None,
        context: [QnARequestContext] = None,
        qna_id: int = None,
        is_test: bool = False,
        ranker_type: str = RankerTypes.DEFAULT,
        strict_filters_join_operator: str = JoinOperator.AND,
    ):
        """
        Parameters:
        -----------
        score_threshold (float):
            The minimum score threshold, used to filter returned results.
            Values range from score of 0.0 to 1.0.
        timeout (int):
            The time in milliseconds to wait before the request times out.
        top (int):
            The number of ranked results to return.
        strict_filters ([Metadata]):
            Filters to use on queries to a QnA knowledge base, based on a
            QnA pair's metadata.
        context ([QnARequestContext]):
            The context of the previous turn.
        qna_id (int):
            Id of the current question asked (if available).
        is_test (bool):
            A value indicating whether to call test or prod environment of a knowledge base.
        ranker_type (str):
            The QnA ranker type to use.
        strict_filters_join_operator (str):
            A value indicating how strictly you want to apply strict_filters on QnA pairs' metadata.
            For example, when combining several metadata filters, you can determine if you are
            concerned with all filters matching or just at least one filter matching.
        """
        self.score_threshold = score_threshold
        self.timeout = timeout
        self.top = top
        self.strict_filters = strict_filters or []
        self.context = context
        self.qna_id = qna_id
        self.is_test = is_test
        self.ranker_type = ranker_type
        self.strict_filters_join_operator = strict_filters_join_operator
