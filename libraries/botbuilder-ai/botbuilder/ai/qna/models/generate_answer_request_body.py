# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model
from .metadata import Metadata


class GenerateAnswerRequestBody(Model):
    """ Question used as the payload body for QnA Maker's Generate Answer API. """

    _attribute_map = {
        "question": {"key": "question", "type": "str"},
        "top": {"key": "top", "type": "int"},
        "score_threshold": {"key": "scoreThreshold", "type": "float"},
        "strict_filters": {"key": "strictFilters", "type": "[Metadata]"},
    }

    def __init__(
        self,
        question: str,
        top: str,
        score_threshold: float,
        strict_filters: [Metadata],
        **kwargs
    ):
        """
        Parameters:
        -----------

        name: Metadata name. Max length: 100.

        value: Metadata value. Max length: 100.
        """

        super().__init__(**kwargs)

        self.question = question
        self.top = top
        self.score_threshold = score_threshold
        self.strict_filters = strict_filters
