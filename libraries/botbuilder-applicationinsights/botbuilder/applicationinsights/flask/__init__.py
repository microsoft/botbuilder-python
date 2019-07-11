# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Flask Application Insights package."""

from .flask_telemetry_middleware import BotTelemetryMiddleware, retrieve_flask_body

__all__ = ["BotTelemetryMiddleware", "retrieve_flask_body"]
