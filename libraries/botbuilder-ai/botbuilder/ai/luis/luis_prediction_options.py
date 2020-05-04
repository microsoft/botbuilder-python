# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.

from botbuilder.core import BotTelemetryClient, NullTelemetryClient


class LuisPredictionOptions:
    """
    Optional parameters for a LUIS prediction request.
    """

    def __init__(
        self,
        bing_spell_check_subscription_key: str = None,
        include_all_intents: bool = None,
        include_instance_data: bool = None,
        log: bool = None,
        spell_check: bool = None,
        staging: bool = None,
        timeout: float = 100000,
        timezone_offset: float = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
        log_personal_information: bool = False,
    ):
        self.bing_spell_check_subscription_key: str = bing_spell_check_subscription_key
        self.include_all_intents: bool = include_all_intents
        self.include_instance_data: bool = include_instance_data
        self.log: bool = log
        self.spell_check: bool = spell_check
        self.staging: bool = staging
        self.timeout: float = timeout
        self.timezone_offset: float = timezone_offset
        self.telemetry_client: BotTelemetryClient = telemetry_client
        self.log_personal_information: bool = log_personal_information
