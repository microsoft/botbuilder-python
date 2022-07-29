# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Application Insights Telemetry Processor for Bots."""
from typing import List

from .django.django_telemetry_processor import DjangoTelemetryProcessor
from .flask.flask_telemetry_processor import FlaskTelemetryProcessor
from .processor.telemetry_processor import TelemetryProcessor


class BotTelemetryProcessor(TelemetryProcessor):
    """Application Insights Telemetry Processor for Bot"""

    def __init__(self, processors: List[TelemetryProcessor] = None):
        self._processors: List[TelemetryProcessor] = (
            [
                DjangoTelemetryProcessor(),
                FlaskTelemetryProcessor(),
            ]
            if processors is None
            else processors
        )

    def can_process(self) -> bool:
        for processor in self._processors:
            if processor.can_process():
                return True

        return False

    def get_request_body(self) -> str:
        for inner in self._processors:
            if inner.can_process():
                return inner.get_request_body()

        return super().get_request_body()
