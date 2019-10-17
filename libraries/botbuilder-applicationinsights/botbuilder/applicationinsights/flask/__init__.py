# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Flask Application Insights package."""

from .flask_telemetry_middleware import BotTelemetryMiddleware

__all__ = ["BotTelemetryMiddleware"]
