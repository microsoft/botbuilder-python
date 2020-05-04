# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import BotTelemetryClient, NullTelemetryClient


class LuisRecognizerOptions:
    def __init__(
        self,
        include_api_results: bool = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
        log_personal_information: bool = False,
    ):
        self.include_api_results = include_api_results
        self.telemetry_client = telemetry_client
        self.log_personal_information = log_personal_information
