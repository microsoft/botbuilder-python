# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model
from typing import Dict


class IntentScore(Model):
    _attribute_map = {
        'score': {'key': 'score', 'type': 'float'},
        'properties': {'key': 'properties', 'type': '{object}'},
    }

    def __init__(self, score: float = None, properties: Dict[str, object] = {}, **kwargs):
        super(IntentScore, self).__init__(**kwargs)
        self.score = score
        self.properties = properties
