# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.core import BotTelemetryClient, NullTelemetryClient
from .luis_recognizer_options import LuisRecognizerOptions


class LuisRecognizerOptionsV3(LuisRecognizerOptions):
    def __init__(
        self,
        include_all_intents: bool = False,
        include_instance_data: bool = True,
        log: bool = True,
        prefer_external_entities: bool = True,
        datetime_reference: str = None,
        dynamic_lists: List = None,
        external_entities: List = None,
        slot: str = "production",
        version: str = None,
        include_api_results: bool = True,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
        log_personal_information: bool = False,
    ):
        super().__init__(
            include_api_results, telemetry_client, log_personal_information
        )
        self.include_all_intents = include_all_intents
        self.include_instance_data = include_instance_data
        self.log = log
        self.prefer_external_entities = prefer_external_entities
        self.datetime_reference = datetime_reference
        self.dynamic_lists = dynamic_lists
        self.external_entities = external_entities
        self.slot = slot
        self.version: str = version
