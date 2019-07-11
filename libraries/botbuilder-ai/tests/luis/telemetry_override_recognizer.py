# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict

from botbuilder.ai.luis import LuisRecognizer, LuisTelemetryConstants
from botbuilder.core import RecognizerResult, TurnContext


class TelemetryOverrideRecognizer(LuisRecognizer):
    def __init__(self, *args, **kwargs):
        super(TelemetryOverrideRecognizer, self).__init__(*args, **kwargs)

    def on_recognizer_result(
        self,
        recognizer_result: RecognizerResult,
        turn_context: TurnContext,
        telemetry_properties: Dict[str, str] = None,
        telemetry_metrics: Dict[str, float] = None,
    ):
        if "MyImportantProperty" not in telemetry_properties:
            telemetry_properties["MyImportantProperty"] = "myImportantValue"

        # Log event
        self.telemetry_client.track_event(
            LuisTelemetryConstants.luis_result, telemetry_properties, telemetry_metrics
        )

        # Create second event.
        second_event_properties: Dict[str, str] = {
            "MyImportantProperty2": "myImportantValue2"
        }
        self.telemetry_client.track_event("MySecondEvent", second_event_properties)
