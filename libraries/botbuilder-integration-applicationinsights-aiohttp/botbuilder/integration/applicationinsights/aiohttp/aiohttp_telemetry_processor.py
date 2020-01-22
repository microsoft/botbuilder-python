# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Telemetry processor for aiohttp."""
import sys

from botbuilder.applicationinsights.processor.telemetry_processor import (
    TelemetryProcessor,
)
from .aiohttp_telemetry_middleware import retrieve_aiohttp_body


class AiohttpTelemetryProcessor(TelemetryProcessor):
    def can_process(self) -> bool:
        return self.detect_aiohttp()

    def get_request_body(self) -> str:
        if self.detect_aiohttp():
            return retrieve_aiohttp_body()
        return None

    @staticmethod
    def detect_aiohttp() -> bool:
        """Detects if running in aiohttp."""
        return "aiohttp" in sys.modules
