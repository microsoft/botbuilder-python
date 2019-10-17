# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Telemetry processor for Django."""
import sys

from ..processor.telemetry_processor import TelemetryProcessor
from .bot_telemetry_middleware import retrieve_bot_body


class DjangoTelemetryProcessor(TelemetryProcessor):
    def can_process(self) -> bool:
        return self.detect_django()

    def get_request_body(self) -> str:
        if self.detect_django():
            # Retrieve from Middleware cache
            return retrieve_bot_body()
        return None

    @staticmethod
    def detect_django() -> bool:
        """Detects if running in django."""
        return "django" in sys.modules
