# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model

from botbuilder.schema import HealthResults


class HealthCheckResponse(Model):
    _attribute_map = {
        "health_results": {"key": "healthResults", "type": "HealthResults"},
    }

    def __init__(self, *, health_results: HealthResults = None, **kwargs) -> None:
        super(HealthCheckResponse, self).__init__(**kwargs)
        self.health_results = health_results
