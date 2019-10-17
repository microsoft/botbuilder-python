# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Telemetry processor for Flask."""
import sys

from ..processor.telemetry_processor import TelemetryProcessor
from .flask_telemetry_middleware import retrieve_flask_body


class FlaskTelemetryProcessor(TelemetryProcessor):
    def can_process(self) -> bool:
        return self.detect_flask()

    def get_request_body(self) -> str:
        if self.detect_flask():
            return retrieve_flask_body()
        return None

    @staticmethod
    def detect_flask() -> bool:
        """Detects if running in flask."""
        return "flask" in sys.modules
