# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Django Application Insights package."""

from . import common
from .bot_telemetry_middleware import BotTelemetryMiddleware
from .logging import LoggingHandler
from .middleware import ApplicationInsightsMiddleware


__all__ = [
    "BotTelemetryMiddleware",
    "ApplicationInsightsMiddleware",
    "LoggingHandler",
    "create_client",
]


def create_client():
    """Returns an :class:`applicationinsights.TelemetryClient` instance using the instrumentation key
    and other settings found in the current Django project's `settings.py` file."""
    return common.create_client()
