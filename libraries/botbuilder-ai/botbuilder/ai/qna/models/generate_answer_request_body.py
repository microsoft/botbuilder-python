# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class GenerateAnswerRequestBody(Model):
    """Question used as the payload body for QnA Maker's Generate Answer API."""

    _attribute_map = {
        "question": {"key": "question", "type": "str"},
        "top": {"key": "top", "type": "int"},
        "score_threshold": {"key": "scoreThreshold", "type": "float"},
        "strict_filters": {"key": "strictFilters", "type": "[Metadata]"},
        "context": {"key": "context", "type": "QnARequestContext"},
        "qna_id": {"key": "qnaId", "type": "int"},
        "is_test": {"key": "isTest", "type": "bool"},
        "ranker_type": {"key": "rankerType", "type": "RankerTypes"},
        "strict_filters_join_operator": {
            "key": "strictFiltersCompoundOperationType",
            "type": "str",
        },
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.question = kwargs.get("question", None)
        self.top = kwargs.get("top", None)
        self.score_threshold = kwargs.get("score_threshold", None)
        self.strict_filters = kwargs.get("strict_filters", None)
        self.context = kwargs.get("context", None)
        self.qna_id = kwargs.get("qna_id", None)
        self.is_test = kwargs.get("is_test", None)
        self.ranker_type = kwargs.get("ranker_type", None)
        self.strict_filters_join_operator = kwargs.get(
            "strict_filters_join_operator", None
        )
