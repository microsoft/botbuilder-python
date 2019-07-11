# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict

from botbuilder.ai.luis import LuisRecognizer, LuisTelemetryConstants
from botbuilder.core import RecognizerResult, TurnContext


class OverrideFillRecognizer(LuisRecognizer):
    def __init__(self, *args, **kwargs):
        super(OverrideFillRecognizer, self).__init__(*args, **kwargs)

    def on_recognizer_result(
        self,
        recognizer_result: RecognizerResult,
        turn_context: TurnContext,
        telemetry_properties: Dict[str, str] = None,
        telemetry_metrics: Dict[str, float] = None,
    ):
        properties = super(OverrideFillRecognizer, self).fill_luis_event_properties(
            recognizer_result, turn_context, telemetry_properties
        )

        if "MyImportantProperty" not in properties:
            properties["MyImportantProperty"] = "myImportantValue"

        # Log event
        self.telemetry_client.track_event(
            LuisTelemetryConstants.luis_result, properties, telemetry_metrics
        )

        # Create second event.
        second_event_properties: Dict[str, str] = {
            "MyImportantProperty2": "myImportantValue2"
        }
        self.telemetry_client.track_event("MySecondEvent", second_event_properties)
