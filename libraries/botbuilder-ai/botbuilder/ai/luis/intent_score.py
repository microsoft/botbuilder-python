# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict


class IntentScore(object):
    """
    Score plus any extra information about an intent.
    """

    def __init__(self, score: float = None, properties: Dict[str, object] = {}):
        self.score: float = score
        self.properties: Dict[str, object] = properties
