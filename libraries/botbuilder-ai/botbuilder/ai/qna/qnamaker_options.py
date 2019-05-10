# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .metadata import Metadata

# figure out if 300 milliseconds is ok for python requests library...or 100000
class QnAMakerOptions:
    def __init__(
        self, 
        score_threshold: float = 0.0,
        timeout: int = 0,
        top: int = 0,
        strict_filters: [Metadata] = []
    ):
        self.score_threshold = score_threshold
        self.timeout = timeout
        self.top = top
        self.strict_filters = strict_filters