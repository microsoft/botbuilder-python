# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .models import Metadata, QnARequestContext
from .models.ranker_types import RankerTypes

# figure out if 300 milliseconds is ok for python requests library...or 100000
class QnAMakerOptions:
    def __init__(
        self,
        score_threshold: float = 0.0,
        timeout: int = 0,
        top: int = 0,
        strict_filters: [Metadata] = None,
        context: [QnARequestContext] = None,
        qna_id: int = None,
        is_test: bool = False,
        ranker_type: bool = RankerTypes.DEFAULT,
    ):
        self.score_threshold = score_threshold
        self.timeout = timeout
        self.top = top
        self.strict_filters = strict_filters or []
        self.context = context
        self.qna_id = qna_id
        self.is_test = is_test
        self.ranker_type = ranker_type
