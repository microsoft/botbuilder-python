# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .metadata import Metadata

class QueryResult:
    def __init__(self, questions: str, answer: str, score: float, metadata: [Metadata], source: str, id: int):
        self.questions = questions,
        self.answer = answer,
        self.score = score,
        self.metadata = Metadata,
        self.source = source
        self.id = id