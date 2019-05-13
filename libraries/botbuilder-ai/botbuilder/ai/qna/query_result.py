# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .metadata import Metadata

class QueryResult:
    def __init__(self, 
    questions: [str], 
    answer: str, 
    score: float, 
    metadata: [Metadata], 
    source: str, 
    id: int,
    context=None
):
        self.questions = questions,
        self.answer = answer,
        self.score = score,
        self.metadata = list(map(lambda meta: Metadata(**meta), metadata)),
        self.source = source
        self.id = id

        # 4.4 multi-turn
        self.context = context
