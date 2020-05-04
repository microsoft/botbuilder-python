# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import BotTelemetryClient, NullTelemetryClient
from .luis_recognizer_options import LuisRecognizerOptions


class LuisRecognizerOptionsV2(LuisRecognizerOptions):
    def __init__(
        self,
        bing_spell_check_subscription_key: str = None,
        include_all_intents: bool = None,
        include_instance_data: bool = True,
        log: bool = True,
        spell_check: bool = None,
        staging: bool = None,
        timeout: float = 100000,
        timezone_offset: float = None,
        include_api_results: bool = True,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
        log_personal_information: bool = False,
    ):
        super().__init__(
            include_api_results, telemetry_client, log_personal_information
        )
        self.bing_spell_check_subscription_key = bing_spell_check_subscription_key
        self.include_all_intents = include_all_intents
        self.include_instance_data = include_instance_data
        self.log = log
        self.spell_check = spell_check
        self.staging = staging
        self.timeout = timeout
        self.timezone_offset = timezone_offset
