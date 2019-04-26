# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import Activity
from .query_result import QueryResult

# Should we set the options=None in TraceInfo? (not optional in node)
class QnAMakerTraceInfo:
    def __init__(
        self, 
        message: Activity, 
        query_results: [QueryResult], 
        knowledge_base_id, 
        score_threshold, 
        top, 
        strict_filters
    ):
        self.message = message,
        self.query_results = query_results,
        self.knowledge_base_id = knowledge_base_id,
        self.score_threshold = score_threshold,
        self.top = top,
        self.strict_filters = strict_filters