# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class QueryResult(Model):
    """Represents an individual result from a knowledge base query."""

    _attribute_map = {
        "questions": {"key": "questions", "type": "[str]"},
        "answer": {"key": "answer", "type": "str"},
        "score": {"key": "score", "type": "float"},
        "metadata": {"key": "metadata", "type": "[Metadata]"},
        "source": {"key": "source", "type": "str"},
        "id": {"key": "id", "type": "int"},
        "context": {"key": "context", "type": "QnAResponseContext"},
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions = kwargs.get("questions", None)
        self.answer = kwargs.get("answer", None)
        self.score = kwargs.get("score", None)
        self.metadata = kwargs.get("metadata", None)
        self.source = kwargs.get("source", None)
        self.context = kwargs.get("context", None)
        self.id = kwargs.get("id", None)  # pylint: disable=invalid-name
